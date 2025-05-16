"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import environ

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))

application = get_wsgi_application()
