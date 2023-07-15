from django.urls import path
from . import views
urlpatterns = [
    path('/add/', views.add_event, name="add"),
    path('/events/',views.event_page, name="events"),
    path('/page/<int:id>', views.page, name="page")
]