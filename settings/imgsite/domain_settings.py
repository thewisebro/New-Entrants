# SITE ID corressponding to Channel i (Internet) or people.iitr.ernet.in
SITE_ID = 2
SITE = 'internet'

try:
  from .local_settings import *
except ImportError:
  pass
