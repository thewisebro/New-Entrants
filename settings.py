# Django settings for channeli project.

import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)

# Email Settings
EMAIL_HOST = '192.168.180.11'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASS = ''

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

# Add apps to python path
sys.path.append(PROJECT_ROOT + '/apps')

# Add third_party_apps to python path
sys.path.append(PROJECT_ROOT + '/third_party_apps')

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'channeli',                   # Or path to database file if using sqlite3.
                                          # The following settings are not used with sqlite3:
    'USER': 'channeli',
    'PASSWORD': 'channeli',
    'HOST': '192.168.121.5',                           # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
    'PORT': '',                           # Set to empty string for default.
  }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# POP3 Server host
POP3_HOST = '192.168.180.11'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

DATE_INPUT_FORMATS = ('%d-%m-%Y', '%d/%m/%Y')
DATETIME_INPUT_FORMATS = ('%d-%m-%Y %H:%M', '%d/%m/%Y %H:%M')
TIME_INPUT_FORMATS = ('%H:%M','%H:%M:%S')

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media') + os.sep

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute filesystem path to NAS media.
NAS_MEDIA_ROOT = '/home/apps/nas/'

# Public URL of NAS folder
NAS_PUBLIC_URL = 'http://www.iitr.ac.in/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_root') + os.sep

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/' # This should be /static/ to make admin's static files available.

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
  # Put strings here, like "/home/html/static" or "C:/www/django/static".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
  os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# 'django.contrib.staticfiles.finders.DefaultStorageFinder',
  'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!v@yt*jnnatgsh$t2!d0-9*mh(6tm4dxst*ypwp6)gxo2qg-em'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
# 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'api.middlewares.DelegateMiddleware',
  # Uncomment the next line for simple clickjacking protection:
  # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

import django.conf.global_settings as DEFAULT_SETTINGS

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
  'api.context_processors.custom',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
  # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
  os.path.join(PROJECT_ROOT, 'templates'),
)

DJANGO_CONTRIB_APPS = (
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.admin',
  'django.contrib.humanize',
  # Uncomment the next line to enable admin documentation:
  # 'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
#  'debug_toolbar',
  'rest_framework',
  'crispy_forms',
  'taggit',
  'taggit_autocomplete',
  'threadedcomments',
  # placed here because threadedcomments is to be placed before it
  'django.contrib.comments',
  'compressor',
  'django_extensions',
)

CHANNELI_APPS = (
  'nucleus',
  'api',
  'reporting',
  'crop_image',
  'groups',
  'events',
  'lostfound',
)

INSTALLED_APPS = DJANGO_CONTRIB_APPS + THIRD_PARTY_APPS + CHANNELI_APPS

COMMENTS_APP = 'threadedcomments'

AUTH_USER_MODEL = 'nucleus.User'

CRISPY_TEMPLATE_PACK = 'uni_form'

CRISPY_CLASS_CONVERTERS = {
  'datewidget': "textinput textInput",
  'timewidget': "textinput textInput",
  'datetimewidget': "textinput textInput",
}

COMPRESS_PRECOMPILERS = (
  ('text/sass', 'sass -I '+PROJECT_ROOT+'/static/ --cache-location '+\
   PROJECT_ROOT+'/.sass-cache --compass {infile} {outfile}'),
)

SHELL_PLUS = "ipython"

SESSION_COOKIE_NAME = 'PHPSESSID'
SESSION_ENGINE = 'nucleus.session'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'filters': {
    'require_debug_false': {
      '()': 'django.utils.log.RequireDebugFalse'
    }
  },
  'formatters': {
    'verbose': {
      'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
      #'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
    },
    'simple': {
      'format': '%(levelname)s %(message)s'
    },
  },
  'handlers': {
    'mail_admins': {
      'level': 'ERROR',
      'filters': ['require_debug_false'],
      'class': 'django.utils.log.AdminEmailHandler'
    },
    'lostfound_file_logger': {
      'level':'DEBUG',
      'class':'logging.handlers.TimedRotatingFileHandler',
      'formatter': 'verbose',
      'filename' : os.path.join(PROJECT_ROOT, 'logs/lostfound'),
      'when'     : 'midnight',
      'backupCount':365
    },
  },
  'loggers': {
    'django.request': {
      'handlers': ['mail_admins'],
      'level': 'ERROR',
      'propagate': True,
    },
    'lostfound': {
      'handlers':['lostfound_file_logger'],
      'level':'INFO'
    },
  }
}
