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