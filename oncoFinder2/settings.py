# -*- coding: utf-8 -*-

import os
import socket

PROJECT_DIR = os.path.realpath(os.path.dirname(__file__))

LOGIN_URL = "/login"

if socket.gethostname() == '127.0.0.1':
    DEBUG = False
else:
    DEBUG = True   
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['127.0.0.1:8000', '127.0.0.1', ]

ADMINS = (
   ('Mikhail', 'mihkorz@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'oncoFinder2',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'of_mysql_pass',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = ( os.path.join(PROJECT_DIR, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w!1tq3xml_enj80)j4pjjj(a4b9em3tht3wo8=(i&amp;m^xxj*-om'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'oncoFinder2.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'oncoFinder2.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates')
)

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
     
    #third-party apps 
    'gunicorn',
    'debug_toolbar',
    'south',
    
    
    #internal apps
    'website',
    'profiles',
    'database',
    'metabolism',
    'mouse'

)

if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {
        
        'INTERCEPT_REDIRECTS': False,
    }

###################### Application settings #######################################
PATIENT_UPLOAD_FILES_CONTENT_TYPES = (
    'text/plain',
    'text/csv',
    'text/comma-separated-values',
    'text/tsv',
    'application/csv',
    'application/txt',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/octet-stream',
)

PATIENT_UPLOAD_FILES_SUPPORTED_FORMATS = (
    'txt',
    'csv',
    'xls',
    'xlsx',
)

###################### Logging settings #######################################
LOG_ROOT = os.path.join(PROJECT_DIR, '..', 'log')
if not os.path.exists(LOG_ROOT):
    os.mkdir(LOG_ROOT)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'msg': {
            'format': '%(asctime)s %(message)s'
        }
    },
    'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse',
         }
     },
    'handlers': {
        'log_file': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, 'oncofinder.log'),
            'encoding': 'utf-8',
            'maxBytes': 1024*1024, # 1 MB
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'console':{
            'level': 'WARN',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'formatter': 'msg'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'propagate': False
        },
        'oncoFinder': {
            'handlers': ['log_file', 'syslog', 'mail_admins'],
            'level': 'INFO',
        },
        'oncoFinder.email': {
            'handlers': ['log_file', 'syslog'],
            'level': 'INFO',
            'propagate': False
        },
        'oncoFinder.clean': {
            'handlers': ['syslog'],
            'level': 'INFO',
            'propagate': False
        },
        'oncoFinder.API': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False
        },
        'oncoFinder.auth': {
            'handlers': ['log_file', 'syslog'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
##################### Environment-specific Settings ############################



if socket.gethostname() == 'mikhail' or socket.gethostname() == 'mikhailComp':
    try:
        from settings_local import *
    except ImportError:
        pass