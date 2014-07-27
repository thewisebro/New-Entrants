from django.conf import settings

ARTIST_PIC_DIR = settings.JUKEBOX_MEDIA_ROOT
ALBUMART_DIR = settings.JUKEBOX_MEDIA_ROOT
SONG_DIR = settings.JUKEBOX_MEDIA_ROOT +'songs/english/'
SONGS_JSON_FILE = settings.JUKEBOX_MEDIA_ROOT +'songs_json/songs.json'
ARTISTS_JSON_FILE = settings.JUKEBOX_MEDIA_ROOT +'songs_json/artistsnew.json'
ALBUMS_JSON_FILE = settings.JUKEBOX_MEDIA_ROOT +'songs_json/albumsnew.json'

ALL_ALBUMS_JSON_FILE = settings.JUKEBOX_MEDIA_ROOT + 'songs_json/all_albums.json'
ALL_ARTISTS_JSON_FILE = settings.JUKEBOX_MEDIA_ROOT + 'songs_json/all_artists.json'


lang_choices = {
      'eng' : 'English',
      'hindi' : 'Hindi',
      'tamil':'Tamil',
      'telugu':'Telugu',
      'punjabi':'Punjabi',
      'mal':'Malyali'
      }

banned_artists = []      # artists like 'Movies', 'Hindi'
