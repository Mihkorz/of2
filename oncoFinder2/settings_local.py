"""
Machine-specific settings.
"""
from settings_default import *


if socket.gethostname() in ['mikhail', 'mikhailComp', 'ubu-node304']:

    INTERNAL_IPS = ('127.0.0.1',)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'oncoFinder2',                      # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': 'mysqlpass',                  # Not used with sqlite3.
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        },
        'food': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'insilico_8_september_2',                      # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': 'mysqlpass',                  # Not used with sqlite3.
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

    if socket.gethostname() == 'ubu-node304':
        DATABASES['default']['NAME'] = 'oncoFinder2'
        DATABASES['default']['PASSWORD'] = '123'

    #INSTALLED_APPS += ('debug_toolbar',)

    APP_ENVIRONMENT = 'DEV'

    if socket.gethostname() == 'ubu-node304':
        LOGGING['loggers']['oncoFinder']['level'] = 'DEBUG'


if socket.gethostname() == 'of-uat':
    APP_ENVIRONMENT = 'UAT'
