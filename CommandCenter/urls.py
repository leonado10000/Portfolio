from django.urls import path
from . import views

app_name = 'logs'

urlpatterns = [
    path("", views.index, name="commandcenter-index"),
    path("addrecord", views.addrecord, name="commandcenter-addrecord"),
    path("testrecord", views.testrecord, name="commandcenter-testrecord"),
    # The Cron Job trigger (keep this hidden/secured)
    path('api/cron/process-bronze/', views.process_bronze_to_silver, name='cron_process'),

    # The Main Dashboard
    path('cc/logs/', views.logs_dashboard, name='dashboard'),
    
    # APIs powering the dashboard UI
    path('cc/logs/api/map-data/', views.map_data_api, name='map_data'),
    path('cc/logs/api/toggle-flag/', views.toggle_manual_flag, name='toggle_flag'),
]