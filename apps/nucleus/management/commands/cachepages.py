from django.core.management.base import BaseCommand, CommandError
from django.test import Client

class Command(BaseCommand):
   args = ''
   help = 'Generates cached pages for production'

   def handle(self, *args, **options):
     c = Client()
     response = c.get('/')
     f = open('production/cached_pages/index.html','w+')
     f.write(response.content)
     f.close()
     self.stdout.write('Successfully generated cached pages')
