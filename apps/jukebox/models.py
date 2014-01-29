import nucleus
import settings
import utils
import datetime

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
  year = models.IntegerField(max_length=4, default = datetime.datetime.today().year)
  album_art = models.ImageField(upload_to=JC.ALBUMART_DIR, max_length=MC.TEXT_LENGTH)
  def __unicode__(self):
    return self.album

class Song(models.Model):
  id_no = models.IntegerField(max_length=MC.TEXT_LENGTH)
  upload_storage = FileSystemStorage(location=JC.SONG_DIR, base_url='/uploads')
  song = models.CharField(max_length=MC.TEXT_LENGTH)          # Dispay name of Song
  file_name = models.FileField(upload_to=content_file_name, storage=upload_storage, max_length=1000)     # Name of The Song on the disk
  album = models.ForeignKey(Album, null=True)
  # ^ export album_art
  artists = models.ManyToManyField(Artist)              # Multiple Artists (feat.)
  genres = models.ManyToManyField(Genre)                 # Multiple Genres
  lang_choices = (
      ('eng' , 'English'),
      ('hindi' , 'Hindi')
  )
  language = models.CharField(max_length=10, choices=lang_choices)
#  date_added = models.DateField(auto_now_add=True)        # For the date item is added
#  date_created = models.DateField()                       # For the date mentioned in the album
  count = models.PositiveIntegerField(default=0)
  score = models.PositiveIntegerField(default=0)          # For Trending Songs
  def __unicode__(self):
    return self.song

  def save(self, *args, **kwargs):
    """
      To save extra artists in respective Album object
    """
    super(Song,self).save(*args, **kwargs)              # Save the usual way
    if self.album:
      album_artists = set(self.album.artists.all())       # Set used as list '-' was creating problem
      artists = set(self.artists.all())
      diff = list(artists-album_artists)
      album_artists = list(album_artists) + diff          # list addition
      self.album.artists = album_artists
      self.album.save()

  def delete(self,*args,**kwargs):
    """
      To delete extra artists in respective Album object
    """
    if self.album:
      rm_songs = self.album.song_set.all().exclude(id = self.id)      # rm -> Remaining things
      rm_artists_id = rm_songs.values_list('artists',flat='true')
      rm_artists = set(Artist.objects.filter(id__in=rm_artists_id))
      album_artists = set(self.album.artists.all())
      artists = set(self.artists.all())
      diff = artists - rm_artists
      album_artists = album_artists - diff
      self.album.artists = list(album_artists)
      self.album.save()
    super(Song,self).delete(*args,**kwargs)                         # delete the usual way


class Playlist(models.Model):
  person = models.ForeignKey(nucleus.models.User, related_name='jukebox_person')
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  songs = models.TextField(null=True, blank=True)                                     # TextField:-> Large amount of songs with 'b' in between
  private = models.BooleanField(default=True)
  liked_by = models.ManyToManyField(nucleus.models.User, related_name='jukebox_playlist_likes')
  def __unicode__(self):
    return self.name

  def insert(self, songs_pk, index=-1):
    """
      To insert songs in playlist(self) at index=index
      songs_pk is the list of selected songs primary key
    """
    if self.songs == '':
      songs = songs_pk
      songs = 'b'.join(str(v) for v in songs)
      self.songs = songs
      self.save()
    else:
      songs_in = self.songs.split('b')
      songs_in = map(int, songs_in)
      songs_diff = list(utils.unique(songs_pk, songs_in))         # unique in utils.py, songs_diff-> songs to be added
      if index == -1 :
        songs = songs_in + songs_diff
      else:
        songs = songs_in[:index] + songs_diff + songs_in[index:]
      songs = 'b'.join(str(v) for v in songs)
      self.songs = songs
      self.save()

  def remove(self,songs_pk):
    """
      To remove songs in playlist(self) : no index required
      songs_pk is the list of selected songs primary key
    """
    songs_in = self.songs.split('b')
    songs_in = map(int, songs_in)
    songs_diff = list(utils.unique(songs_in, songs_pk))         # unique in utils.py, songs_diff-> remaining songs
    songs = 'b'.join(str(v) for v in songs_diff)
    self.songs = songs
    self.save()



