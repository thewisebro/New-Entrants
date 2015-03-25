"""
  Management command ./manage.py cachejukebox
"""
from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser
from mutagen.easyid3 import EasyID3
import mutagen
import urllib2
import re
import os
import wget
import socket
import json
print 'here'
from django.core.management.base import BaseCommand, CommandError
import nucleus
from jukebox.models import Song
from jukebox.serializers import *
print 'hereeeee'

count=0
htm = HTMLParser()
arr = []
artists_all = {}

def add_song_list(song,st):
  son = open('/home/pankaj/scripts/songs_lista.txt','a+')
  sono = open('/home/pankaj/scripts/songs_list_fulla.txt','a+')
  son.write(song+'\n')
  """art = get_artist(arr[1])
  alb = get_album(arr[2])
  sono.write(art+'::'+alb+'::'+song+'::'+st+'\n')
  """
  son.close()
  sono.close()


def add_error(err,line):
  error = open('/home/pankaj/scripts/songs_errora.txt','a+')
  err = str(err)+'\t'+str(line)
  print err
  error.write(err+'\n')
  error.close()

def xx(x):
  if len(x)!=0:
    return x[0]
  else:
    return

def fa(x):
  return x!=None

def get_artist(st):
  st = st.split('(')
  st = map(lambda x: x.strip(), st)
  st.pop()
  return '('.join(st)

def get_album(st):
  st = st.split('(')
  st = map(lambda x: x.strip(), st)
  le = len(st)
  while le>0:
    a = st[le-1]
    a = a[:len(a)-1]
    if not a.isdigit():
      break
    st.pop()
    le = le-1
  return ' ('.join(st)

def hindi(x):
  try:
    print x.text
    st = htm.unescape(x.text)
#print get_artist(arr[1]),get_album(arr[2])
    url = htm.unescape('http://songpk.mobi/'+x['href'])
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    scr = soup.findAll('script')
    if len(scr) > 0:
      link=scr[0]
      for w in scr:
        if (w.text).find('download1.php')>=0:
          link = w
      link=link.text[link.text.find('http://songpk.mobi/dgmob/downloadfile'):]
      link=link[:link.find('.mp3')+4]
    #album = get_album(arr[2])
    get_album(st)
    album = st.split('(').pop()
    if album.rfind(')') >= 0:
      album = album[:album.rfind(')')]
    print album
    song = get_artist(st)
    print '\n'+song
    song = song.split('-')
    song = map(lambda x: x.strip(), song)
    directory = '/'.join(['/home/pankaj/songsmedia/','hindisongs',album])
    if not os.path.exists(directory):
      os.makedirs(directory)
    os.chdir(directory)
    print 'download starting'
    print link
    filename = wget.download(link)
    os.rename(filename,st+'.mp3')
    print st+'.mp3'

    song = '-'.join(song)
#pri genre
    add_song_list(st,link)
  except Exception as e:
    add_error(e,x)
    pass

def english(x):
  try:
    st = htm.unescape(x.text)
#print get_artist(arr[1]),get_album(arr[2])
    url = htm.unescape('http://englishsong.in/'+x['href'])
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    scr = soup.findAll('script')
    link=soup.getText()[soup.getText().find('http://englishsong.in/glory-data/downloadfile'):]
    link=link[:link.find('.mp3')+4]
    song = st.split('(')[0]
    print '\nsong: '+song
    song = song.split('-')
    song = map(lambda x: x.strip(), song)
    directory = '/'.join(['/home/pankaj/songsmedia/songs'])
    if not os.path.exists(directory):
      os.makedirs(directory)
    os.chdir(directory)
    print 'download starting'
    print link, '\n'
    filename = wget.download('http://englishsong.in/'+link)
    os.rename(filename,st+'.mp3')
    print st+'.mp3'

    song = '-'.join(song)
    try:
      songid = EasyID3(st+'.mp3')
    except Exception as e:
      songid = EasyID3()
    date = songid.get('date','')
#pri date
    genre = songid.get('genre','')
#pri genre
    """ try:
#rm_tists = list(set(artists)-set(artists_all))
#artts_all += rm_artists
#forrt in artists:
      artists_m = Artist.objects.get_or_create(artist=artist)[0]
#artts_m = Artist.objects.filter(artist__in=artists)
#pri artists
# Foalbum
      print 'artists m    ',artists_m.artist
      album_m = Album.objects.get_or_create(album=album)[0]
      print album_m.album
      album_m.artists.add(artists_m)
      try:
        album_m.year = int(date[0])
      except Exception as e:
        write_artists()
        add_error(e,'date  '+song)
      album_m.save()
      print album_m.artists.all()
# FoGenre
      genre_m = Genre.objects.get_or_create(genre=genre)[0]
# FoSong
      song_m = Song.objects.get_or_create(id_no=0, song=song, language='eng')[0]
      song_m.file_name.name = artist+'/'+album+'/'+st+'.mp3'
      song_m.genres.add(genre_m)
      song_m.album = album_m                                                             # -< Not Working
      song_m.artists.add(artists_m)
      song_m.save()
      print song_m.song
      add_song_list(st,link)
    except Exception as e:
      add_error(e, song)
      pass
      """
  except Exception as e:
    add_error(e,x)
    pass


def download_url(url):
  try:
    url = htm.unescape(url)
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    nex = soup.findAll('td',{'colspan':'2'})
    nex = map(lambda x: x.findAll('a'),nex)
    nex = map(xx,nex)
    nex = filter(fa,nex)
#mapf,nex)
    for n in nex:
      try:
        if 'englishsong.in' in url:
          english(n)
        else:
          hindi(n)
      except KeyboardInterrupt:
        if 'englishsong.in' in url:
          english(n)
        else:
          hindi(n)
      except:
        pass
    nex = map(lambda aa: aa['href'],nex)
  except Exception as e:
    add_error(e,'  url problem')
    pass
  return



class Command(BaseCommand):
  help = 'Downloads the link you give for an album and asks for its language, artist and album name'

  def add_arguments(self, parser):
    parser.add_argument('dlink', nargs='\t', type=str)

    def handle(self, *args, **options):
      print 'here'
      for dlink in options['dlink']:
        print dlink
        try:
          download_url(dlink)
        except :
          raise CommandError('Error in downloading\n "%s"\n\n' % dlink)
