# SITE ID corressponding to Channel i (Intranet)
SITE_ID = 1
SITE = 'intranet'

try:
  from .local_settings import *
except ImportError:
  pass
