#!/usr/bin/env python
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# Add apps and lib directories to PYTHONPATH
sys.path = [
    os.path.join(ROOT, 'apps'),
    os.path.join(ROOT, 'lib'),
    # add /lib/* paths here for submodules
] + sys.path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sejm20.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
