from settings.development import *

PRODUCTION = True
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
  '172.25.55.5',
  '172.25.55.156',
  '.channeli.in',
  '.iitr.ernet.in',
]

SESSION_COOKIE_HTTPONLY = True

# Add file logging to loggers
LOGGING['loggers']['channel-i_logger']['handlers'].append('file_logger')
LOGGING['loggers']['lostfound']['handlers'].append('lostfound_file_logger')
LOGGING['loggers']['buysell']['handlers'].append('buysell_file_logger')

try:
  from production.settings import *
except ImportError:
  pass
