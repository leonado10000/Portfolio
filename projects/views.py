from django.shortcuts import render

# Create your views here.
def codebunny_landing(request):
    return render(request, "codebunny/codebunny_landing.html")