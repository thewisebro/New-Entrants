from django.core.management.base import BaseCommand
from feeds.helper import ModelFeedMeta

class Command(BaseCommand) :

  help = 'Prints the sql triggers code for feed generation.\nSyntax : ./manage.py feedsqltriggers app [model_name]'

  def handle(self,*argv,**options):
    if len(argv) == 1:
      app = argv[0]
      modelfeeds = filter(lambda mf : mf.Meta.app==app and mf.Meta.php_app, ModelFeedMeta.modelfeeds)
    elif len(argv) == 2:
      app,model_name = argv
      modelfeeds = filter(lambda mf : mf.Meta.app==app and mf.Meta.php_app and mf.Meta.model.__name__==model_name, ModelFeedMeta.modelfeeds)
    for mf in modelfeeds:
      mf.mysql_trigger()
