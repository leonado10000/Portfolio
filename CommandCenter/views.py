from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from .models import bronzelogs
import requests

def index(request):
    return render(request, "CommandCenter/index.html")

@csrf_exempt
def addrecord(request):
    if request.method == "POST":
        bronzelogs.objects.create(
            userip=request.POST.get('userip', ''),
            user=request.POST.get('user', 'Anonymous'),
            actionmessage=request.POST.get('actionmessage', ''),
            source=request.POST.get('source', '')
        )
        return HttpResponse("Record added successfully.")
    elif request.method == "GET":
        token = get_token(request)
        return JsonResponse({"csrfToken": token})
    return HttpResponse("Method not allowed", status=405)

def testrecord(request):
    action_function_name = "Testing"
    school_mate_map = {
        'all_current_terms':'Checking terms',
        'marksheet_view':'Viewing marksheet',
        'student_scorecard':'Viewing student scorecard',
        'scorecard_pdf_download':'Downloading scorecard',
        'checks_index':'Notebook checking class list',
        'list_checks':'Listing all checks of a class',
        'nb_checking':'Notebook checking interface',
        'student_checks_detail':'Viewing student notebook check details',
        'all_students':'Listing all students for notebook checking',
        'class_list':'Listing all classes',
        'student_detail':'Viewing student details',
        'student_create':'Creating a new student',
        'student_edit':'Editing student details',
        'student_delete':'Deleting a student',
        'student_list_by_batch':'Listing students by batch',
    }
    source = ""
    if action_function_name in school_mate_map:
        source = "Schoolmate"
    else:
        source = "Others"
    try:
        url = "https://rahul-jangra-leonado10000.vercel.app/cmd/addrecord"
        res = requests.post(
            url,
            data={
                'userip': request.META.get('REMOTE_ADDR', ''),
                'actionmessage': school_mate_map.get(action_function_name, ''),
                'source': source,
                'user': request.user.username if request.user.is_authenticated else 'Anonymous',
            }
        )
        return index(request)
    except Exception as e:
        return index(request)

import json
import logging
import urllib.request
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.db.models import Count, Min, Max, F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import bronzelogs, IPProfile

logger = logging.getLogger(__name__)

# --- Dashboard Views ---

@staff_member_required
def logs_dashboard(request):
    """
    Renders the main dashboard page at /cc/logs/
    """
    total_logs = IPProfile.objects.aggregate(total=Count('id'))['total'] or 0
    
    profiles = IPProfile.objects.all().order_by('-last_visit')
    
    auto_bots = [p for p in profiles if p.is_bot]
    bot_percentage = round((len(auto_bots) / max(len(profiles), 1)) * 100, 1)

    context = {
        'total_logs': total_logs, # Now represents total UNIQUE IPs tracked
        'bot_percentage': bot_percentage,
        'flagged_ips': profiles[:20], 
        'recent_logs': [], # Removed detailed stream since we delete raw logs
    }
    return render(request, 'logs/dashboard.html', context)


@staff_member_required
def map_data_api(request):
    """
    Provides GeoJSON/JSON data for the frontend Leaflet.js world map.
    """
    profiles = IPProfile.objects.exclude(latitude__isnull=True).values(
        'ip_address', 'is_manual_flagged', 'is_auto_flagged', 
        'city', 'country', 'latitude', 'longitude', 'total_visits'
    )
    
    map_points = []
    for p in profiles:
        is_manual = p['is_manual_flagged']
        is_bot = is_manual if is_manual is not None else p['is_auto_flagged']
        
        map_points.append({
            "lat": p['latitude'],
            "lng": p['longitude'],
            "ip": p['ip_address'],
            "city": p['city'],
            "country": p['country'],
            "is_bot": is_bot,
            "visit_count": p['total_visits']
        })
        
    return JsonResponse({"points": map_points})


@staff_member_required
@csrf_exempt
def toggle_manual_flag(request):
    """
    API endpoint for the dashboard to manually flag/unflag an IP.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ip_address = data.get('ip_address')
            status = data.get('status') 

            profile = get_object_or_404(IPProfile, ip_address=ip_address)
            
            if status == 'true' or status is True:
                profile.is_manual_flagged = True
            elif status == 'false' or status is False:
                profile.is_manual_flagged = False
            else:
                profile.is_manual_flagged = None
                
            profile.save()
            return JsonResponse({"success": True, "current_bot_status": profile.is_bot})

        except Exception as e:
             return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "POST required"}, status=405)


# --- Helper Functions ---

def get_geoip_data(ip_address):
    """
    Fetches GeoIP data for a given IP.
    Updated to use freeipapi.com as it is more permissive for serverless/backend requests.
    Allows 60 requests per minute for free without a key.
    """
    if not ip_address or ip_address in ['127.0.0.1', 'localhost']:
        return {"country": "Local", "city": "Local"}

    try:
        url = f"https://freeipapi.com/api/json/{ip_address}"
        # Adding a User-Agent is still good practice to prevent basic blocking
        req = urllib.request.Request(url, headers={'User-Agent': 'DjangoPortfolioApp'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            
            # freeipapi returns the requested IP in the response if successful
            if data and data.get('ipAddress'):
                return {
                    "country": data.get("countryName", "Unknown"),
                    "city": data.get("cityName", "Unknown"),
                    "latitude": data.get("latitude"),
                    "longitude": data.get("longitude")
                }
    except Exception as e:
        logger.warning(f"GeoIP lookup failed for {ip_address}: {e}")
    
    return {"country": "Unknown", "city": "Unknown", "latitude": None, "longitude": None}

def analyze_for_bot(ip_address, batch_count, current_total_visits):
    """
    Revised bot detection based on aggregate profile data rather than checking individual logs.
    """
    # If this batch alone brought in over 50 requests for this IP, it's highly suspicious.
    if batch_count > 50:
        return True, f"Velocity spike: {batch_count} reqs in single batch"
        
    # If lifetime visits exceed 1000, probably a scraper.
    if current_total_visits + batch_count > 1000:
        return True, f"Excessive lifetime visits: > 1000"

    return False, None


# --- The Main Vercel Cron View ---

@csrf_exempt
def process_bronze_to_silver(request):
    """
    Groups raw bronze logs into IP profiles, updating counts and timestamps.
    Deletes the raw logs afterwards to save database space.
    """
    auth_header = request.headers.get('Authorization')
    expected_secret = getattr(settings, 'VERCEL_CRON_SECRET', None)
    if expected_secret and auth_header != f"Bearer {expected_secret}":
         return JsonResponse({"error": "Unauthorized"}, status=401)

    # 1. Fetch raw logs and group by IP in the database
    # This single query gets the count, min timestamp, and max timestamp for every IP
    grouped_logs = bronzelogs.objects.values('userip').annotate(
        batch_count=Count('id'),
        first_in_batch=Min('timestamp'),
        last_in_batch=Max('timestamp')
    ) # Process up to 100 unique IPs per cron run

    if not grouped_logs:
        return JsonResponse({"status": "success", "message": "No new logs to process", "processed_count": 0})

    processed_ips = 0

    try:
        with transaction.atomic():
            for log_data in grouped_logs:
                ip = log_data['userip']
                batch_count = log_data['batch_count']
                first_ts = log_data['first_in_batch']
                last_ts = log_data['last_in_batch']

                # Try to find existing profile
                profile = IPProfile.objects.filter(ip_address=ip).first()

                if profile:
                    # UPDATE EXISTING PROFILE
                    
                    # 1. Grab the current integer value before we overwrite it with an F() expression
                    current_visits_int = profile.total_visits
                    
                    # 2. Now it's safe to assign the F() expression for the database update
                    profile.total_visits = F('total_visits') + batch_count
                    
                    # Keep the absolute earliest first_visit
                    if first_ts < profile.first_visit:
                        profile.first_visit = first_ts
                    # Keep the absolute latest last_visit
                    if last_ts > profile.last_visit:
                        profile.last_visit = last_ts
                        
                    # 3. Pass the integer we grabbed earlier to the bot analyzer
                    is_bot, reason = analyze_for_bot(ip, batch_count, current_visits_int)
                    
                    if is_bot and not profile.is_auto_flagged:
                        profile.is_auto_flagged = True
                        profile.auto_flag_reason = reason
                        
                    profile.save(update_fields=['total_visits', 'first_visit', 'last_visit', 'is_auto_flagged', 'auto_flag_reason', 'updated_at'])
                
                else:
                    # CREATE NEW PROFILE
                    # Only do the slow GeoIP lookup if we've never seen this IP before
                    geo_data = get_geoip_data(ip)
                    is_bot, reason = analyze_for_bot(ip, batch_count, 0)
                    
                    IPProfile.objects.create(
                        ip_address=ip,
                        total_visits=batch_count,
                        first_visit=first_ts,
                        last_visit=last_ts,
                        country=geo_data.get('country'),
                        city=geo_data.get('city'),
                        latitude=geo_data.get('latitude'),
                        longitude=geo_data.get('longitude'),
                        is_auto_flagged=is_bot,
                        auto_flag_reason=reason
                    )
                
                processed_ips += 1

            # 3. Cleanup: Delete the raw logs we just processed
            # We delete any bronze log matching the IPs we just handled, up to the max timestamp we processed
            # This prevents deleting a log that came in *during* this cron execution
            ips_processed = [log['userip'] for log in grouped_logs]
            bronzelogs.objects.filter(userip__in=ips_processed, timestamp__lte=last_ts).delete()

    except Exception as e:
        logger.error(f"Error processing profiles: {e}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({
        "status": "success", 
        "message": f"Successfully processed and aggregated {processed_ips} unique IPs",
    })