from settings.development import *

COMPRESS_ENABLED = True

try:
  from production.settings import *
except ImportError:
  pass
