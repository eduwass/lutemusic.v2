"""
LuteMusic management command with subcommands.

Usage:
    python manage.py lutemusic download_json_files
    python manage.py lutemusic <subcommand> [options]
"""

import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'LuteMusic management command with various subcommands'

    def add_arguments(self, parser):
        """Define subcommands and their arguments"""
        subparsers = parser.add_subparsers(
            dest='subcommand',
            help='Available subcommands',
            required=True
        )
        
        # download_json_files subcommand
        download_parser = subparsers.add_parser(
            'download_json_files',
            help='Download JSON files and save them to data/lutemusic/'
        )
        download_parser.add_argument(
            '--target-dir',
            type=str,
            default='lutemusic',
            help='Target directory within project data folder (default: lutemusic)'
        )
        download_parser.add_argument(
            '--force',
            action='store_true',
            help='Overwrite existing files'
        )

    def handle(self, *args, **options):
        """Route to appropriate subcommand handler"""
        subcommand = options['subcommand']
        
        if subcommand == 'download_json_files':
            return self.handle_download_json_files(**options)
        else:
            raise CommandError(f"Unknown subcommand: {subcommand}")

    def handle_download_json_files(self, **options):
        """
        Download JSON files and save them to media directory.
        
        Equivalent to the WordPress CLI command:
        wp lutemusic download_json_files
        """
        # Define files to download
        files = {
            'insts.json': 'https://www.lutemusic.org/insts.json',
            'types.json': 'https://www.lutemusic.org/types.json',
            'settings.json': 'https://www.lutemusic.org/settings.json',
            'names.json': 'https://www.lutemusic.org/names.json',
        }
        
        # Determine target directory - use project data folder
        target_dir_name = options['target_dir']
        project_root = Path(settings.BASE_DIR)
        target_dir = project_root / 'data' / target_dir_name
        
        # Create directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)
        
        self.stdout.write(f"Downloading JSON files to: {target_dir}")
        
        success_count = 0
        error_count = 0
        
        for filename, url in files.items():
            target_file = target_dir / filename
            
            # Check if file exists and handle overwrite
            if target_file.exists() and not options['force']:
                self.stdout.write(
                    self.style.WARNING(f"File {filename} already exists. Use --force to overwrite.")
                )
                continue
            
            try:
                # Download file
                self.stdout.write(f"Downloading {filename} from {url}...")
                
                with urllib.request.urlopen(url) as response:
                    data = response.read()
                
                # Convert to string for encoding detection and JSON validation
                try:
                    # Try to decode as UTF-8 first
                    text_data = data.decode('utf-8')
                except UnicodeDecodeError:
                    # If UTF-8 fails, try with latin-1 and convert to UTF-8
                    self.stdout.write(
                        self.style.WARNING(f"Encoding of {filename} is not UTF-8. Converting to UTF-8.")
                    )
                    text_data = data.decode('latin-1').encode('utf-8').decode('utf-8')
                
                # Validate JSON
                try:
                    json_data = json.loads(text_data)
                except json.JSONDecodeError as e:
                    raise CommandError(f"Invalid JSON in {filename}: {e}")
                
                # Save file
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(text_data)
                
                self.stdout.write(
                    self.style.SUCCESS(f"Downloaded and saved {filename} to {target_dir}")
                )
                success_count += 1
                
                # Log the action
                logger.info(f"Downloaded {filename} from {url} to {target_file}")
                
            except urllib.error.URLError as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to download {url}: {e}")
                )
                error_count += 1
                
            except OSError as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to save {filename} to {target_dir}: {e}")
                )
                error_count += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Unexpected error with {filename}: {e}")
                )
                error_count += 1
        
        # Summary
        total_files = len(files)
        self.stdout.write(
            self.style.SUCCESS(
                f"\nCompleted: {success_count}/{total_files} files downloaded successfully"
            )
        )
        
        if error_count > 0:
            self.stdout.write(
                self.style.WARNING(f"Errors: {error_count} files failed to download")
            )
        
        return f"Downloaded {success_count}/{total_files} JSON files successfully" 