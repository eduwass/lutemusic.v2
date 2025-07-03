"""
Core utilities for calling management commands from web code.
"""

from django.core.management import call_command
from django.core.management.base import CommandError
from io import StringIO
import logging

logger = logging.getLogger(__name__)


def run_hello_command(name="World", shout=False, count=1):
    """
    Call the hello management command from web code.
    
    Args:
        name (str): Name to greet
        shout (bool): Whether to shout
        count (int): Number of greetings
        
    Returns:
        dict: Result with success status and output
    """
    try:
        # Capture command output
        output = StringIO()
        
        # Call the management command
        call_command(
            'hello',
            name=name,
            shout=shout,
            count=count,
            stdout=output,
            stderr=output
        )
        
        # Get the output
        command_output = output.getvalue()
        
        return {
            'success': True,
            'output': command_output,
            'message': f'Hello command executed successfully for {name}'
        }
        
    except CommandError as e:
        logger.error(f"Command error: {e}")
        return {
            'success': False,
            'error': str(e),
            'message': 'Command failed'
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            'success': False,
            'error': str(e),
            'message': 'Unexpected error occurred'
        }


def run_management_command(command_name, *args, **kwargs):
    """
    Generic utility to run any management command from web code.
    
    Args:
        command_name (str): Name of the management command
        *args: Positional arguments for the command
        **kwargs: Keyword arguments for the command
        
    Returns:
        dict: Result with success status and output
    """
    try:
        output = StringIO()
        
        call_command(
            command_name,
            *args,
            stdout=output,
            stderr=output,
            **kwargs
        )
        
        return {
            'success': True,
            'output': output.getvalue(),
            'message': f'{command_name} executed successfully'
        }
        
    except CommandError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        } 