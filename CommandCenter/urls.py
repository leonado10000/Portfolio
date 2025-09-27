from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="commandcenter-index"),
    path("addrecord", views.addrecord, name="commandcenter-addrecord"),
    path("testrecord", views.testrecord, name="commandcenter-testrecord"),
]