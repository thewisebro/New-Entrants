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
    #ht(path, 'national')
    #ht(path, 'sports')

    """
    hindu.Entertainment(path)
    toi.Entertainment(path)
    ie.Entertainment(path)
    msn.Entertainment(path)
    bbc.Entertainment(path)
    """

    bbc.selectAll(path)
    hindu.selectAll(path)
    toi.selectAll(path)
    ie.selectAll(path)
    msn.selectAll(path)
    yahoo.selectAll(path)

    """
    hindu.Technology(path)
    toi.Technology(path)
    ie.Technology(path)
    bbc.Technology(path)
    hindu.Education(path)
    toi.Education(path)
    ie.Education(path)
    hindu.Health(path)
    toi.Health(path)
    ie.Health(path)
    bbc.Health(path)
    """

    return HttpResponse("Task Completed!!")
  except Exception as e:
    return HttpResponse(e)


if __name__ == '__main__':
  load_data()

