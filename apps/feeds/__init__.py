from django.conf import settings

for app in settings.FEED_APPS:
  __import__(app+".feed")
