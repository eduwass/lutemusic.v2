"""
Web views demonstrating how to call management commands from web interface.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core.utils import run_hello_command, run_management_command


def home(request):
    """Simple home page"""
    return render(request, 'web/home.html', {
        'title': '🎵 LuteMusic'
    })


@require_http_methods(["GET", "POST"])
def run_command_view(request):
    """
    Example: Run management commands from web interface
    
    GET: Show form
    POST: Execute command
    """
    if request.method == 'POST':
        # Get parameters from form/API
        name = request.POST.get('name', 'Web User')
        shout = request.POST.get('shout') == 'on'
        count = int(request.POST.get('count', 1))
        
        # Call the management command
        result = run_hello_command(name=name, shout=shout, count=count)
        
        if request.headers.get('Content-Type') == 'application/json':
            # API response
            return JsonResponse(result)
        else:
            # Web response
            return render(request, 'web/command_result.html', {
                'result': result,
                'name': name
            })
    
    # GET: Show the form
    return render(request, 'web/run_command.html')


def api_run_command(request):
    """
    API endpoint to run management commands
    
    POST /api/run-command/
    {
        "command": "hello",
        "name": "API User",
        "shout": true,
        "count": 3
    }
    """
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            command = data.get('command', 'hello')
            
            if command == 'hello':
                result = run_hello_command(
                    name=data.get('name', 'API'),
                    shout=data.get('shout', False),
                    count=data.get('count', 1)
                )
            else:
                # Generic command runner
                result = run_management_command(command, **data)
            
            return JsonResponse(result)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON'
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    }, status=405)
