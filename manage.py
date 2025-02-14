#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess


def format_code():
    """Format code using black."""
    try:
        subprocess.run(["black", "."], check=True)
        subprocess.run(["djlint", "templates/", "--reformat"], check=True)
        print("Code formatted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error formatting code: {e}")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unilnk.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) > 1 and sys.argv[1] == "format":
        format_code()
    else:
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
