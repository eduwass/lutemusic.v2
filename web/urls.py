"""
URL configuration for web app
"""
from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.home, name='home'),
    path('run-command/', views.run_command_view, name='run_command'),
    path('api/run-command/', views.api_run_command, name='api_run_command'),
] 