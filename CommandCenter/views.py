from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from .models import bronzelogs
import requests
from django.test import Client

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
    client = Client(enforce_csrf_checks=True)
    client.get("/cmd/addrecord/")  # get CSRF cookie
    csrftoken = client.cookies['csrftoken'].value

    res = client.post(
        "/cmd/addrecord/",
        {'actionmessage': 'Test action', 'source': 'Test source'},
        HTTP_X_CSRFTOKEN=csrftoken
    )

    return HttpResponse(f"Test POST status: {res.status_code}, text: {res.content}")
