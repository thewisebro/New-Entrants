"""
WSGI config for channeli project_path.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, sys

configuration_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(os.path.dirname(configuration_path))
sys.path.append(project_path)

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.channeli.prod_settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
def ApplicationWrapper(application):
  def wrapped_application(environ, start_response):
    if environ['PATH_INFO'] == '/':
      f = open(project_path+'/static_root/CACHE_PAGES/index.html','r')
      response_body = f.read()
      f.close()
      status = '200 OK'
      response_headers = [('Content-Type', 'text/html'),
                            ('Content-Length', str(len(response_body)))]
      start_response(status, response_headers)
      return [response_body]
    else:
      return application(environ, start_response)
  return wrapped_application

application = ApplicationWrapper(application)
