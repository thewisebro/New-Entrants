# SITE ID corressponding to Channel i (Internet) or people.iitr.ernet.in
SITE_ID = 2
SITE = 'internet'

from ..common.settings import MIDDLEWARE_CLASSES
MIDDLEWARE_CLASSES += (
    'api.middlewares.SiteMiddleware',
)

try:
  from .local_settings import *
except ImportError:
  pass
