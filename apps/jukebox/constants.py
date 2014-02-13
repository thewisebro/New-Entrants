from django.conf import settings

ARTIST_PIC_DIR = '/home/songsmedia/'
ALBUMART_DIR = '/home/songsmedia/'
SONG_DIR = '/home/pankaj/jukebox_songs/newestsongs/'
SONGS_JSON_FILE = '/home/pankaj/channeli/songs.json'
ARTISTS_JSON_FILE = '/home/pankaj/channeli/artistsnew.json'
ALBUMS_JSON_FILE = '/home/pankaj/channeli/albumsnew.json'

ALL_ALBUMS_JSON_FILE = settings.MEDIA_ROOT + 'jukebox/all_albums.json'
ALL_ARTISTS_JSON_FILE = settings.MEDIA_ROOT + 'jukebox/all_artists.json'
