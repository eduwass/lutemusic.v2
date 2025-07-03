"""
Web views for the LuteMusic application.
"""

from django.shortcuts import render


def home(request):
    """Simple home page"""
    return render(request, 'web/home.html', {
        'title': '🎵 LuteMusic'
    })
