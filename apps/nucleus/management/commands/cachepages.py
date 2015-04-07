import os

from django.core.management.base import BaseCommand, CommandError
from django.test import Client
from django.conf import settings

class Command(BaseCommand):
   args = ''
   help = 'Generates cached pages for production'

   def handle(self, *args, **options):
     c = Client()
     response = c.get('/')
     cache_dir = settings.PROJECT_ROOT + '/static_root/CACHE_PAGES'
     if not os.path.exists(cache_dir):
       os.mkdir(cache_dir)
     f = open(cache_dir+'/index.html','w+')
     f.write(response.content)
     f.close()
     self.stdout.write('Successfully generated cached pages')
