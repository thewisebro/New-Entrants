from settings.development import *

PRODUCTION = True
DEBUG = False
TEMPLATE_DEBUG = DEBUG

try:
  from production.settings import *
except ImportError:
  pass
