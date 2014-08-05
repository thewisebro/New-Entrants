#!/usr/bin/python

import os, sys
#sys.path.append(os.path.join(os.path.abspath("../../../..")))
#from django.core.management import setup_environ
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channeli.settings")
from django.conf import settings
from news.channels import hindu, ie, msn, toi, yahoo, bbc #, nyt

def load_data():
  #path = os.path.dirname(__file__)
  #path = os.path.join(path, 'xml_files/')
  #print(path)
  path = settings.NEWS_XML_ROOT
  os.chdir(settings.NEWS_IMAGES_ROOT)
  #print(os.getcwd())
  try:
    bbc.selectAll(path)
    hindu.selectAll(path)
    toi.selectAll(path)
    ie.selectAll(path)
    msn.selectAll(path)
    yahoo.selectAll(path)
    return True
  except Exception as e:
    print e
    return False


if __name__ == '__main__':
  load_data()

