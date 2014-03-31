from django_cron import CronJobBase, Schedule
from jukebox.models import *

def score_half(song):
  song.score /= 2
  song.save()

class ScoreHalf(CronJobBase):
  RUN_EVERY_MINS = 1 # every 24 hours

  schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
  code = 'jukebox.scorehalf'
  def do(self):
    map(score_half, Song.objects.exclude(score__lte=0))
    pass    # do your thing here
