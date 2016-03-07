from mutagen.easyid3 import EasyID3
from glob import glob

from django.core.files import File
from django.conf import settings

from jukebox.models import *

songs_root = settings.JUKEBOX_MEDIA_ROOT + 'Ndirect/'
songs_split = len(songs_root.split('/'))

def add_songs(lang):
  count=0
  err = []
  err1 = []
  for artist_dir in glob(songs_root+'*'):
    try:
      artist = Artist.objects.get_or_create(artist=artist_dir.split('/')[songs_split-1], language=lang)[0]
    except:
      artist = Artist.objects.filter(artist=artist_dir.split('/')[songs_split-1], language=lang)[0]
      err.append(artist_dir.split('/')[songs_split-1])
    try:
      print artist.artist, '       artist        created'
    except:
      pass
    for album_dir in glob(artist_dir+'/*'):
      album = Album.objects.get_or_create(album=album_dir.split('/')[songs_split], language=lang)[0]
      album.artists.add(artist)
      album.latest=True
      album.datetime_created = album.datetime_created.now()
      album.save()
      try:
        image = glob(album_dir+'/*.jpg')
        if len(image):
          image = image[0]
          album.album_art.save(image.split('/')[songs_split+1].encode('ascii','ignore'), File(open(image)), save=True)
      except:
        pass
        
      try:
        print album.album, '       album                 made'
      except:
        pass
      for song_dir in glob(album_dir+'/*.mp3'):
          title = song_dir.split('/')[songs_split+1]
          title = title[:title.find('.mp3')]
          try:
            song = EasyID3(song_dir)
            title = song['title'][0]
          except:
            pass
          title = title.split('-')
          title = '-'.join(title[:len(title)-1])
          title = title.strip()
          song = Song.objects.get_or_create(song = title, album=album, language=lang)
          if not song[1]:
            try:
              print song[0].song, '   already present at\t', song[0].file_name.name
            except:
              pass
            continue
          song = song[0]
          song.artists.add(artist)
          try:
            song.file_name.save((song_dir.split('/')[songs_split+1]).encode('ascii', 'ignore'), File(open(song_dir)), save=True)
            song.save()
            count += 1
            try:
              print song.song, '      song  saved  ', song_dir, '\tcount\t', count
            except:
              print '\t\t\t\tcount\t', count
          except:
            print 'Error in saving \t', song_dir.split('/')[songs_split]
            try:
              song.file_name.save((title).encode('ascii', 'ignore'), File(open(song_dir)), save=True)
              song.save()
              count += 1
              try:
                print song.song, '      song  saved  ', song_dir, '\tcount\t', count
              except:
                print '\t\t\t\tcount\t', count
            except:
              try:
                print 'Error in saving \t', title
              except:
                pass
              song.delete()

def add_songs_direct(lang):
  count = 0
  for artist_dir in glob(songs_root+'*'):
    try:
      artist = Artist.objects.get_or_create(artist=(artist_dir.split('/')[songs_split-1].split('-')[0]).strip(), language=lang)[0]
      print artist.artist, '       artist        created'
    except:
      artist = Artist.objects.filter(artist=(artist_dir.split('/')[songs_split-1].split('-')[0]).strip(), language=lang)[0]
      print artist.artist, '       artist        once created'
    try:
      album = Album.objects.get_or_create(album=(artist_dir.split('/')[songs_split-1].split('-')[1]).strip(), language=lang)[0]
    except:
      album = Album.objects.filter(album=(artist_dir.split('/')[songs_split-1].split('-')[1]).strip(), language=lang)[0]
    album.artists.add(artist)
    album.latest = True
    album.save()
    print album.album, '       album                 made'
    try:
      image = glob(artist_dir+'/*.jpg')
      if len(image):
        image = image[0]
        album.album_art.save(image.split('/')[songs_split].encode('ascii','ignore'), File(open(image)), save=True)
    except:
        pass

    for song_dir in glob(artist_dir+'/*.mp3'):
        title = song_dir.split('/')[songs_split]
        title = title[:title.find('.mp3')]
        try:
          song = EasyID3(song_dir)
          title = song['title'][0]
        except:
          pass
        title = title.split('-')
        title = '-'.join(title[:len(title)-1])
        title = title.strip()
        try:
          print title
        except:
          pass
        song = Song.objects.get_or_create(song = title, album=album, language=lang)
        if not song[1]:
          try:
            print song[0].song, '   already present at\t', song[0].file_name.name
          except:
            pass
          continue
        song = song[0]
        song.artists.add(artist)
        try:
          song.file_name.save((song_dir.split('/')[songs_split]).encode('ascii', 'ignore'), File(open(song_dir)), save=True)
          song.save()
          count += 1
          try:
            print song.song, '      song  saved  ', song_dir, '\tcount\t', count
          except:
            print '\t\t\t\tcount\t', count
        except:
          print 'Error in saving \t', song_dir.split('/')[songs_split]
          try:
            song.file_name.save((title).encode('ascii', 'ignore'), File(open(song_dir)), save=True)
            song.save()
            count += 1
            try:
              print song.song, '      song  saved  ', song_dir, '\tcount\t', count
            except:
              print '\t\t\t\tcount\t', count
          except:
            try:
              print 'Error in saving \t', title
            except:
              pass
            song.delete()
          
