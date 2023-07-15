from django.shortcuts import render

# Create your views here.

def home(request):
        return render(request, 'home.html')

def home2(request):
        return render(request, 'portfolio\home2.html' )