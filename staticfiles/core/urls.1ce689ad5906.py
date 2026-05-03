from django.urls import path
from . import views

urlpatterns = [
    path('', views.func, name="else"),
    path('quests', views.quests, name="quests"),
    path('WebResume', views.WebResume, name="webresume"),
    path('games', views.games_home, name="games_home"),
    path('terminal', views.terminal_view, name="terminal"),
    path('visitors', views.visitors, name="visitors")
]