from django.shortcuts import render
from Portfolio.views import welcoming_user

# Create your views here.
@welcoming_user
def home(request):
    return render(request, 'home.html')