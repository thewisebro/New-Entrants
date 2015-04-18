import os

from django.core.management.base import BaseCommand, CommandError
from feeds.helper import ModelFeedMeta

class Command(BaseCommand):
   args = ''
   help = 'Creates feed for php apps'

   def handle(self, *args, **options):
     event, table, pk = args
     for modelfeed in ModelFeedMeta.modelfeeds:
       model = modelfeed.Meta.model
       if model._meta.db_table == table:
         kwargs = {}
         if event == 'INSERT' or event == 'UPDATE':
           kwargs['instance'] = model.objects.get(pk=int(pk))
           kwargs['created'] = True if event == 'INSERT' else False
           modelfeed.on_save(model,**kwargs)
         else:
           kwargs['pk']=pk
           modelfeed.on_delete(model,**kwargs)
