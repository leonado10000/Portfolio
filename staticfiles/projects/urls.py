from django.urls import path
from .views import codebunny_landing, schoolmate_landing

urlpatterns = [
    path("codebunny", codebunny_landing, name="codebunny_landing"),
    path("schoolmate", schoolmate_landing, name="schoolmate_landing"),
]