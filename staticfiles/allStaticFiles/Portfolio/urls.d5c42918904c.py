from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name="ind"),
    path('project', views.projects, name="projects"),
    path('v2/',views.v2)
]
