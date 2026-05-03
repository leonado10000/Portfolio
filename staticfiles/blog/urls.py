from django.urls import path
from . import views
urlpatterns = [
    path('<int:topic_id>', views.blog, name="blog"),
    path('ban', views.banning, name="ban"),
    path('unban', views.unbanning, name="unban"),
    
]