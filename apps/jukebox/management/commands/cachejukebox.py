import json

from django.core.management.base import BaseCommand, CommandError

from jukebox.models import Artist, Album
from jukebox.serializers import *
from jukebox.constants import ALL_ALBUMS_JSON_FILE, ALL_ARTISTS_JSON_FILE

class Command(BaseCommand):

  def handle(self, *args, **options):
    try:
      if(args[0]=='albums'):
        cache_albums()
      else:
        cache_artists()
    except:
      raise CommandError('Error in caching albums')


artists = {}
count = 0
err = []

def insert_artist(x):
  global count
  try:
    artist = ArtistDescSerializer(x).data
    artists[artist['id']] = artist
    count+=1
    print artist['artist'],'  ',count
  except:
    err.append(x)

def cache_artists():
  global artists
  artists = {}
  global count
  count = 0
  map(insert_artist, Artist.objects.all())
  json.dump(artists,artists_json)
  artists_json = open(ALL_ARTISTS_JSON_FILE,'w+')
  print err

albums = {}

def insert_album(x):
  global count
  try:
    album = AlbumDescSerializer(x).data
    albums[album['id']] = album
    count+=1
    print album['album'],'  ',count
  except:
    err.append(x)

def cache_albums():
  global albums
  albums = {}
  global count
  count = 0
  map(insert_album, Album.objects.order_by('album'))
  albums_json = open(ALL_ALBUMS_JSON_FILE,'w+')
  json.dump(albums,albums_json)
  print err
