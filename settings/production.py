from settings.development import *

try:
  from production.settings import *
except ImportError:
  pass
