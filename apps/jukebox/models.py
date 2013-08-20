import nucleus
import settings

from core import models
from django.core.files.storage import FileSystemStorage
from api import model_constants as MC
from jukebox import constants as JC

# jukebox.models starts




"""
class Person(models.Model):
  person = models.OneToOneField(nucleus.models.Person, related_name='jukebox_person')
  def __unicode__(self):
    return self.person
"""
def content_file_name(instance, filename):
  return '/'.join([instance.album.album, filename])


class Artist(models.Model):
  artist = models.CharField(max_length=MC.TEXT_LENGTH)
  cover_pic = models.ImageField(upload_to=JC.ARTIST_PIC_DIR, max_length=MC.TEXT_LENGTH)
  def __unicode__(self):
    return self.artist

class Genre(models.Model):
  genre = models.CharField(max_length=MC.TEXT_LENGTH)
  def __unicode__(self):
    return self.genre

class Album(models.Model):
  album = models.CharField(max_length=MC.TEXT_LENGTH)
  artists = models.ManyToManyField(Artist, blank=True, null=True)              # Multiple Artists (feat.)
#genres = models.ManyToManyField(Genre)                # Multiple Genres
  album_art = models.ImageField(upload_to=JC.ALBUMART_DIR, max_length=MC.TEXT_LENGTH)
  def __unicode__(self):
    return self.album

class Song(models.Model):
  upload_storage = FileSystemStorage(location=JC.SONG_DIR, base_url='/uploads')
  song = models.CharField(max_length=MC.TEXT_LENGTH)          # Dispay name of Song
  file_name = models.FileField(upload_to=content_file_name, storage=upload_storage, max_length=MC.TEXT_LENGTH)     # Name of The Song on the disk
  album = models.ForeignKey(Album, null=True)
  # ^ export album_art
  artists = models.ManyToManyField(Artist)              # Multiple Artists (feat.)
  genres = models.ManyToManyField(Genre)                 # Multiple Genres
  lang_choices = (
      ('eng' , 'English'),
      ('hindi' , 'Hindi')
  )
  language = models.CharField(max_length=10, choices=lang_choices)
  date_added = models.DateField(auto_now_add=True)        # For the date item is added
  date_created = models.DateField()                       # For the date mentioned in the album
  count = models.PositiveIntegerField(default=0)
  score = models.PositiveIntegerField(default=0)          # For Trending Songs
  def __unicode__(self):
    return self.song

class Playlist(models.Model):
  person = models.ForeignKey(nucleus.models.User, related_name='jukebox_person')
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  songs = models.ManyToManyField(Song)
  private = models.BooleanField(default=True)
  liked_by = models.ManyToManyField(nucleus.models.User, related_name='jukebox_playlist_likes')
  def __unicode__(self):
    return self.name
