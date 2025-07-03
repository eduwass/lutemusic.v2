"""
Example Django management command.

Usage:
    python manage.py hello
    python manage.py hello --name "World"
    python manage.py hello --name "Django" --shout
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Example command that demonstrates Django management command patterns'

    def add_arguments(self, parser):
        """Define command line arguments"""
        parser.add_argument(
            '--name',
            type=str,
            default='World',
            help='Name to greet (default: World)'
        )
        
        parser.add_argument(
            '--shout',
            action='store_true',
            help='Make the greeting LOUD'
        )
        
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help='Number of times to greet'
        )

    def handle(self, *args, **options):
        """Main command logic"""
        name = options['name']
        count = options['count']
        shout = options['shout']
        
        # Example: Access database
        user_count = User.objects.count()
        
        # Create greeting message
        greeting = f"Hello, {name}! You have {user_count} users in the database."
        
        if shout:
            greeting = greeting.upper()
        
        # Output the greeting(s)
        for i in range(count):
            self.stdout.write(
                self.style.SUCCESS(greeting)
            )
        
        # Example: Log the action
        logger.info(f"Greeted {name} {count} times")
        
        return f"Greeted {name} successfully!"  # Can return for web usage 