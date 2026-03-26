from django.urls import path
from .views import codebunny_landing

urlpatterns = [
    path("codebunny", codebunny_landing, name="codebunny_landing")
]