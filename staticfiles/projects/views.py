from django.shortcuts import render
from utils.bronzelogger import bronzelogger

# Create your views here.
@bronzelogger
def codebunny_landing(request):
    return render(request, "codebunny/codebunny_landing.html")

@bronzelogger
def schoolmate_landing(request):
    return render(request, "schoolmate/schoolmate_landing.html")

@bronzelogger
def sockets_chatroom_landing(request):
    return render(request, "sockets_chatroom/sockets_chatroom_landing.html")

@bronzelogger
def autograd_from_scratch_landing(request):
    return render(request, "autograd_from_scratch/autograd_from_scratch_landing.html")