import os

from django.core.management.base import BaseCommand, CommandError
from feeds.models import Feed
from phpapps.models import LectutLectures
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
  args = ''
  help = 'Creates feed for php apps'

  def handle(self, *args, **options):
    c = ContentType.objects.get_for_model(LectutLectures)
    last_feeds = Feed.objects.filter(instance_type=c).order_by('-instance_id')
    if last_feeds.exists():
      last_feed = last_feeds[0]
      last_instance_id = last_feed.instance_id
      for lec in LectutLectures.objects.filter(pk__gt=last_instance_id).order_by('pk'):
        lec.save()
        feed = Feed.objects.get_or_none(instance_type=c, instance_id=lec.pk)
        feed.datetime_created = lec.timestamp
        feed.save()
