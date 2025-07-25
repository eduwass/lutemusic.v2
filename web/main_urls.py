"""
URL configuration for lutemusic project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),  # Include web app URLs
]
