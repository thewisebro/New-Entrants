import os, sys
# Add this line if your script is not in your app directory
sys.path.append('/home/pankaj/channeli/') # If your project is in '/home/user/mysite/polls', you have to put sys.path.append('/home/user/mysite/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'channeli.settings'
from django.conf import settings
from jukebox.models import *

from glob import glob
from HTMLParser import HTMLParser
from mutagen.easyid3 import EasyID3
import mutagen
import re




home = '/home/pankaj/jukebox_songs/newsongs/'
dirs = [x[0] for x in os.walk(home)]
htm = HTMLParser()
dirs = map(lambda x: htm.unescape(x), dirs)
error = open('/home/pankaj/jukebox_scripts/entry_error.txt','w+')

def get_artists(s):
  def my_split(s, seps):
    res = [s]
    for sep in seps:
      s, res = res, []
      for seq in s:
        res += seq.split(sep)
    return res
  art = my_split(s,['ft.','Ft.','feat.','Feat.','feat','Feat','&','ft','Ft',',','vs.','vs','Vs.','Vs','VS.','VS'])
  art = map(lambda x: x.strip().title(),art)
  return art




def is_present(s):
  lis = glob(s+'/*.mp3')
  if(len(lis)):
    return True
  return False

def add_error(err,line):
  error.write(str(err)+'\t'+str(line)+'\n')

def mapin(x):
  if type(x) is list:
    return x[0]
  elif x != '':
# print x
    pass
  return str(x)

def rem(x):
  k = re.compile('www.songslover',re.IGNORECASE)
  x = x.lower()
  m = x.split('-')
  m = map(lambda x: x.strip(),m)
  if k.match(m[-1]):
    m.pop(-1)
  x = '-'.join(m)
  return x.title()

def print_details():
  count = 0
  artists_all = []
  for d in dirs:
    try:
      dir_len = len(d.split('/'))
      if dir_len==7 :
        lis = glob(d+'/*.mp3')
        if len(lis):
          for mp in lis:
            try:
              try:
                song = EasyID3(mp)
              except Exception as e:
                song = EasyID3()
              dir_split = mp.split('/')
              title = song.get('title',dir_split[-1])
              artist = song.get('artist',dir_split[-3])
              album = song.get('album',dir_split[-2])
              date = song.get('date','')
              genre = song.get('genre','')
              pr = [title, artist, album, date, genre]
              pr =map(mapin, pr)
              pr = [dir_split[-1]] + pr
              pr = map(rem,pr)
              st = '\n'.join(pr)
              
# For artists
              artists = get_artists(pr[2])
              rm_artists = list(set(artists)-set(artists_all))
              artists_all += rm_artists
              for art in rm_artists:
                Artist.objects.get_or_create(artist=art)
              artists_m = Artist.objects.filter(artist__in=artists)
              print artists
# For album 
              album_m = Album.objects.get_or_create(album=pr[3])[0]
              print album_m.album
              album_m.artists.add(*artists_m)
              print album_m.artists.all()[0].artist
# For Genre
              genre_m = Genre.objects.get_or_create(genre=pr[5])[0]
# For Song
              song_m = Song.objects.get_or_create(song=pr[1], language='eng')[0]
              song_m.file_name.name = mp
              song_m.genres.add(genre_m)
              song_m.album = album_m                                                             # -< Not Working
              song_m.artists.add(*artists_m)
              song_m.save()
              print song_m.song
              count += 1
              if count==100:
                print "\n\nyo!! next 100 entries done\n\n"

                
            except Exception as e:
              print e + '\t\t\t\terrrrrrrr\n'
              print pr
#return
              add_error(e,mp)
    except Exception as e:
#print e
      add_error(e,mp)
  print "count : "+count


print_details()
