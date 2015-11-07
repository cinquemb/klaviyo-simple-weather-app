from .base import *

DEBUG = True
WUNDERGROUND_KEY = '751b945b05e70eb6'
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.8/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = True


'''
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'KEY_PREFIX': 'klaviyo-dev'
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'klaviyo',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'klaviyo',
        'PASSWORD': 'A5879f1047a9B',
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                      # Set to empty string for default.
    }
}