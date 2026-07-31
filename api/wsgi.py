"""WSGI entry point for production servers (gunicorn, uWSGI).

Usage:
    gunicorn wsgi:app -c gunicorn.conf.py
"""

from app import create_app

app = create_app()