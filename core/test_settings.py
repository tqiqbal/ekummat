"""Isolated settings for local checks; never use the live database in tests."""
from .settings import *  # noqa: F403

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']
SECRET_KEY = 'ekummat-local-tests-only'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
