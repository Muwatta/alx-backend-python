#!/usr/bin/env python3
"""Custom createsuperuser command for custom User model."""

from django.contrib.auth.management.commands import createsuperuser
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(createsuperuser.Command):
    """Custom createsuperuser command."""
    
    def add_arguments(self, parser):
        """Add custom arguments."""
        super().add_arguments(parser)
        # Remove username argument
        parser.add_argument(
            '--noinput',
            '--no-input',
            action='store_false',
            dest='interactive',
            help='Do not prompt the user for input of any kind.',
        )
    
    def handle(self, *args, **options):
        """Handle superuser creation."""
        options['username'] = ''  # Bypass username validation
        super().handle(*args, **options)