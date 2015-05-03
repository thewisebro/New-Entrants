from feeds.helper import ModelFeed
from phpapps.models import *
from django.utils.html import escape
from nucleus.models import Faculty, User
from datetime import datetime
from django.template.loader import render_to_string
import HTMLParser
html_parser = HTMLParser.HTMLParser()

###################### LecTut Feeds #######################

def get_lectut_feed_content(instance, user, upload_type):
  return render_to_string('phpapps/common_feed.html', {
    'user': user,
    'instance': instance,
    'upload_type': upload_type
  })


class LectureFeed(ModelFeed):
  def save(self,instance,created):
    user = User.objects.get(username=instance.faculty_id)
    return {
      'content': get_lectut_feed_content(instance, user, 'lecture'),
      'user': user,
      'link': '/lectut/'
    }

  class Meta:
    model = LectutLectures
    app = "lectut"
    php_app = True

class SolutionFeed(ModelFeed):
  def save(self,instance,created):
    user = User.objects.get(username=instance.faculty_id)
    return {
      'content': get_lectut_feed_content(instance, user, 'solution'),
      'user': user,
      'link': '/lectut/'
    }

  class Meta:
    model = LectutSolutions
    app = "lectut"
    php_app = True

class TutorialFeed(ModelFeed):
  def save(self,instance,created):
    user = User.objects.get(username=instance.faculty_id)
    return {
      'content': get_lectut_feed_content(instance, user, 'tutorial'),
      'user': user,
      'link': '/lectut/'
    }

  class Meta:
    model = LectutTutorials
    app = "lectut"
    php_app = True
