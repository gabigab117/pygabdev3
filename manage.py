#!/usr/bin/env python
import os
import sys

from project.settings.base import env

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        env("DJANGO_SETTINGS_MODULE", default="project.settings.dev"),
    )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
