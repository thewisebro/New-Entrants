from settings.development import *

PRODUCTION = True
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
  '192.168.121.5',
  '.channeli.in',
  '.iitr.ernet.in',
]

try:
  from production.settings import *
except ImportError:
  pass
