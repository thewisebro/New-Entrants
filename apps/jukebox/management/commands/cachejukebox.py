import json

from django.core.management.base import BaseCommand, CommandError

from jukebox.models import Artist, Album
from jukebox.serializers import *

class Command(BaseCommand):
  artists = {}
  artists_json = open('all_artists.json','w+')
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
    global artists,artists_json
    artists = {}
    global count
    count = 0
    map(insert_artist, Artist.objects.all())
    json.dump(artists,artists_json)
    print err

  albums = {}
  albums_json = open('all_albums.json','w+')

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
    global albums,albums_json
    albums = {}
    global count
    count = 0
    map(insert_album, Album.objects.order_by('album'))
    json.dump(albums,albums_json)
    print err

  def add_arguments(self, parser):
    parser.add_argument('cache', nargs='+', type=str)

  def handle(self, *args, **options):
    try:
      if(options['cache'][0]=='albums'):
        cache_albums()
      else:
        cache_artists()
    except:
      raise CommandError('Error in caching albums')
