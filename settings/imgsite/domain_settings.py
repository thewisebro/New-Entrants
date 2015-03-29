# SITE ID corressponding to IMG website (dynamic)
SITE_ID = 3
SITE = 'imgsite'

try:
  from .local_settings import *
except ImportError:
  pass
