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
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import bronzelogs, SilverLogs, FlaggedIP

logger = logging.getLogger(__name__)

# --- Dashboard Views ---

@staff_member_required # Ensures only you (admin) can access this page
def logs_dashboard(request):
    """
    Renders the main dashboard page at /cc/logs/
    """
    # 1. High-level Stats
    total_logs = SilverLogs.objects.count()
    
    # 2. IP Profiles
    flagged_ips = FlaggedIP.objects.all().order_by('-updated_at')
    
    # Calculate bot percentage (using python logic based on the is_bot property)
    auto_bots = [ip for ip in flagged_ips if ip.is_bot]
    bot_percentage = round((len(auto_bots) / max(len(flagged_ips), 1)) * 100, 1)

    # 3. Recent Activity (Stream)
    recent_logs = SilverLogs.objects.select_related('ip_profile').order_by('-timestamp')[:50]

    context = {
        'total_logs': total_logs,
        'bot_percentage': bot_percentage,
        'flagged_ips': flagged_ips[:10], # Top 10 most recently updated IPs
        'recent_logs': recent_logs,
    }
    return render(request, 'logs/dashboard.html', context)


@staff_member_required
def map_data_api(request):
    """
    Provides GeoJSON/JSON data for the frontend Leaflet.js world map.
    Returns latitude and longitude for all logs, colored by bot status.
    """
    # Fetch logs that have coordinates
    logs_with_location = SilverLogs.objects.exclude(latitude__isnull=True).select_related('ip_profile')
    
    map_points = []
    for log in logs_with_location:
        # Determine if this specific log is flagged as a bot via its profile
        is_bot = log.ip_profile.is_bot if log.ip_profile else False
        
        map_points.append({
            "lat": log.latitude,
            "lng": log.longitude,
            "ip": log.userip,
            "city": log.city,
            "country": log.country,
            "is_bot": is_bot,
            "action": log.actionmessage
        })
        
    return JsonResponse({"points": map_points})


@staff_member_required
@csrf_exempt # In a real app, use proper CSRF tokens for POST requests
def toggle_manual_flag(request):
    """
    API endpoint for the dashboard to manually flag/unflag an IP.
    Expects JSON: {"ip_address": "57.148.x.x", "status": true/false/null, "notes": "..."}
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ip_address = data.get('ip_address')
            # status: True (Bot), False (Human), None (Let Auto decide)
            status = data.get('status') 
            notes = data.get('notes', '')

            ip_profile, created = FlaggedIP.objects.get_or_create(ip_address=ip_address)
            
            # Map JS frontend values to Python boolean/None
            if status == 'true' or status is True:
                ip_profile.is_manual_flagged = True
            elif status == 'false' or status is False:
                ip_profile.is_manual_flagged = False
            else:
                ip_profile.is_manual_flagged = None
                
            ip_profile.notes = notes
            ip_profile.save()

            return JsonResponse({"success": True, "current_bot_status": ip_profile.is_bot})

        except Exception as e:
             return JsonResponse({"error": str(e)}, status=400)
             
    return JsonResponse({"error": "POST required"}, status=405)


# --- Helper Functions for Bot Detection ---

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

def analyze_for_bot(ip_address, current_log_timestamp):
    """
    Basic Bot Detection Heuristics.
    Returns: (is_bot: bool, reason: str or None)
    """
    # Heuristic 1: High Velocity (Rate Limiting)
    # If an IP has made more than 30 requests in the last 1 minute, flag it.
    one_minute_ago = current_log_timestamp - timedelta(minutes=1)
    
    # Querying the Bronze logs directly to count recent activity for this IP
    recent_requests = bronzelogs.objects.filter(
        userip=ip_address,
        timestamp__gte=one_minute_ago
    ).count()

    if recent_requests > 30:
        return True, f"High Velocity: {recent_requests} req/min"

    # Heuristic 2: Known Bot Signatures (if User-Agent was logged)
    # If you later add a User-Agent column to BronzeLogs, check it here:
    # bot_signatures = ['bot', 'crawl', 'spider', 'slurp']
    # if any(sig in user_agent.lower() for sig in bot_signatures):
    #     return True, "User-Agent Signature"

    return False, None


# --- The Main Vercel Cron View ---

@csrf_exempt # Required if Vercel calls this via POST without a CSRF token
def process_bronze_to_silver(request):
    """
    This view is intended to be called by a Vercel Cron Job (e.g., every 5 minutes).
    It reads unprocessed Bronze logs, enriches them, runs bot detection, 
    and saves them to the Silver layer.
    """
    
    # Security: Ensure this endpoint is only accessible via Vercel Cron or a valid admin
    # Vercel sends a specific header 'Authorization: Bearer <CRON_SECRET>'
    # You must configure VERCEL_CRON_SECRET in your Django settings/env vars.
    auth_header = request.headers.get('Authorization')
    expected_secret = getattr(settings, 'VERCEL_CRON_SECRET', None)
    
    if expected_secret and auth_header != f"Bearer {expected_secret}":
         return JsonResponse({"error": "Unauthorized"}, status=401)

    # 1. Fetch Unprocessed Logs
    # We find logs in Bronze that do not have a corresponding entry in Silver.
    # Limit to a reasonable batch size (e.g., 100) to prevent Vercel serverless timeouts (usually 10-60s).
    unprocessed_logs = bronzelogs.objects.filter(
        silverlogs__isnull=True
    ).order_by('timestamp')[:100]

    if not unprocessed_logs.exists():
        return JsonResponse({"status": "success", "message": "No new logs to process", "processed_count": 0})

    silver_records_to_create = []
    processed_count = 0

    # We use a transaction to ensure database integrity if the batch fails halfway
    try:
        with transaction.atomic():
            for bronze_log in unprocessed_logs:
                
                # A. Enrichment (GeoIP)
                geo_data = get_geoip_data(bronze_log.userip)
                
                # B. Bot Detection & Profile Linking
                is_bot, bot_reason = analyze_for_bot(bronze_log.userip, bronze_log.timestamp)
                
                # Get or create the IP profile
                ip_profile, created = FlaggedIP.objects.get_or_create(ip_address=bronze_log.userip)
                
                # If the heuristic detected a bot, update the profile (if not already flagged)
                if is_bot and not ip_profile.is_auto_flagged:
                    ip_profile.is_auto_flagged = True
                    ip_profile.auto_flag_reason = bot_reason
                    ip_profile.save()
                
                # C. Prepare Silver Record
                # We instantiate the object but don't save it to the DB yet (for bulk_create)
                silver_record = SilverLogs(
                    bronze_ref=bronze_log,
                    ip_profile=ip_profile,
                    userip=bronze_log.userip,
                    actionmessage=bronze_log.actionmessage,
                    timestamp=bronze_log.timestamp,
                    country=geo_data.get('country'),
                    city=geo_data.get('city'),
                    latitude=geo_data.get('latitude'),
                    longitude=geo_data.get('longitude')
                )
                silver_records_to_create.append(silver_record)
                processed_count += 1

            # 2. Bulk Insert to Silver layer
            # bulk_create is vastly more efficient than calling .save() 100 times.
            SilverLogs.objects.bulk_create(silver_records_to_create)

    except Exception as e:
        logger.error(f"Error processing logs: {e}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({
        "status": "success", 
        "message": f"Successfully processed {processed_count} logs",
        "processed_count": processed_count
    })