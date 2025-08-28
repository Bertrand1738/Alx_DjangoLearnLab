#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
    # Temporarily disable URL checking for migrations
    os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')
    try:
        from django.core.management import execute_from_command_line
        if 'makemigrations' in sys.argv or 'migrate' in sys.argv:
            from django.conf import settings
            settings.ROOT_URLCONF = None
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
