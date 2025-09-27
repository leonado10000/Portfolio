from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from .models import bronzelogs
import requests

def index(request):
    return render(request, "CommandCenter/index.html")

def addrecord(request):
    if request.method == "POST":
        bronzelogs.objects.create(
            userip=request.META.get('REMOTE_ADDR', ''),
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
    url = "https://rahul-jangra-leonado10000.vercel.app/cmd/addrecord"
    session = requests.Session()
    res = session.get(url)
    csrftoken = res.json().get("csrfToken")
    res = session.post(
        url,
        data={
            'actionmessage': 'Test action',
            'source': 'Test source',
            'user': request.user.username if request.user.is_authenticated else 'Anonymous',
        },
        headers={'X-CSRFToken': csrftoken}
    )
    return HttpResponse(f"Test POST status: {res.status_code}, text: {res.text}")
