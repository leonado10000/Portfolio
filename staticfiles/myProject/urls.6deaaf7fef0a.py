from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name="myProject"),
    path('d', views.delete, name="deleteProject")
]