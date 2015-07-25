# SITE ID corressponding to Channel i (Internet) or people.iitr.ernet.in

SITE_ID = 2
SITE = 'INTERNET'

from ..common.settings import MIDDLEWARE_CLASSES
SESSION_COOKIE_DOMAIN = '.iitr.ernet.in'
CSRF_COOKIE_DOMAIN = '.iitr.ernet.in'
MIDDLEWARE_CLASSES += (
    'api.middlewares.SiteMiddleware',
)

try:
  from .local_settings import *

except ImportError:
  pass
