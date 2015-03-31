import random
import os, logging, random
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext
from django.db import transaction
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from games.models import *
from games.canvasgame import CanvasGame
from games.constants import *
from notifications.models import Notification


#Logger information
logger = logging.getLogger('channel-i_logger')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').count() != 0)
def index(request, path=""):
  """
    Display the list of games
  """
  width=80*len(channeli_games)+20
  games = CanvasGame.registered_games
  if path != "":
    raise Http404
  return render_to_response('games/index.html',{'games':games,'total_width':width
      },context_instance=RequestContext(request));

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').count() != 0)
def game(request,gamecode):
  """
    Redirecting to a particular game and display the highscores
  """
  width=80*len(channeli_games)+20
  if gamecode in flash_games:
    return render_to_response('games/flashgame.html',{'range':range(20),'gamecode':gamecode,'gametype':'flash','total_width':width},context_instance=RequestContext(request))
  try:
    games = CanvasGame.registered_games
    game = games[gamecode]
    gsession = str(random.randint(100000000,1000000000))
    authkey = str(random.randint(100000000,1000000000))
    student = request.user.student
    GameSession.objects.filter(student=student).delete()
    GameSession.objects.create(student=student,gamecode=gamecode,gsession=gsession,authkey=authkey,start_time = datetime.today())
    gamescores = GameScore.objects.filter(gamecode=gamecode).order_by('-score')[:50]
    if(len(gamescores)>50):
      last_score=gamescores[49].score
      GameScore.objects.filter(gamecode=gamecode,score__lt=last_score).delete()
    game_content = game.html(gsession = gsession)
    return render_to_response('games/game.html',{'range':range(20),'games':games,'game':game,'game_content':game_content,'gamescores':gamescores,'total_width':width},context_instance=RequestContext(request))
  except Exception as e:
    logger.exception('Games Exception : '+str(e))
    messages.error(request, 'Unknown error has occured. Please try again later. The issue has beeen reported.')
    return render_to_response('games/index.html', {
        }, context_instance=RequestContext(request))

@csrf_exempt
def authenticate(request,gamecode):
  """
    Authenticating the game
  """
  try:
    game = CanvasGame.getGame(gamecode)
    gsession = request.POST['gsession']

    if GameSession.objects.filter(gsession=gsession).count() != 0:
      game_session = GameSession.objects.filter(gsession=gsession)[0]
      passed = game.is_same(gsession=gsession,code=request.POST['wow'])
      return HttpResponse(game_session.authkey if passed else '')
    return HttpResponse('')
  except Exception as e:
    logger.exception('Games Exception : '+str(e))
    return HttpResponse('')

@csrf_exempt
def stop(request,gamecode):
  """
    Stopping the game after it is over
  """
  app='games'
  try:
    game = CanvasGame.getGame(gamecode)
    gsession = request.POST['gsession']
    authkey = request.POST['auth']
    time =  int(request.POST['t'])
    score = int(float(request.POST['s']))
    if GameSession.objects.filter(gsession=gsession).count() != 0:
      game_session = GameSession.objects.filter(gsession=gsession)[0]
      passed = game.is_same(gsession=request.POST['gsession'],code=request.POST['wow'])
      now = datetime.today()
      tdelta = ((now-game_session.start_time.replace(tzinfo=None)).seconds-1-float(time*game.timeinterval)/1000)/(now-game_session.start_time.replace(tzinfo=None)).seconds
      gamescore_set = GameScore.objects.filter(gamecode=gamecode).order_by('-score')
      high_score = None
      if gamescore_set.exists():
        high_score = gamescore_set[0].score
      if passed and game_session.authkey == authkey and abs(tdelta)<2:
        last_gamescore_set = GameScore.objects.filter(student=game_session.student,gamecode=game_session.gamecode).order_by('-score')
        if last_gamescore_set.exists():
          if last_gamescore_set[0].score < score:
            last_gamescore_set.delete()
            GameScore.objects.create(student=game_session.student,gamecode=game_session.gamecode,score=score)
        else:
          GameScore.objects.create(student=game_session.student,gamecode=game_session.gamecode,score=score)
      if high_score and high_score < score:
        url='/games/'+str(gamecode)+'/'
        users=[]
        high_score_list = GameScore.objects.filter(gamecode=gamecode, score=high_score)
        count = 0
        for gamescore in high_score_list:
          if gamescore.student != game_session.student:
            users.append(gamescore.student)
            count += 1
        notif_text = 'Your highscore '+str(high_score)+' in the game '+str(gamecode)+' has been beaten by '
        notif_text += game_session.student.user.html_name()+' with score '+str(score)
        gamescore_objects = GameScore.objects.filter(gamecode=gamecode, score=score)
        pk_id = gamescore_objects[0].pk
        if count > 0:
          Notification.save_notification(app, notif_text, url, users, pk_id)
      game_session.delete()
    return HttpResponse('')
  except Exception as e:
    logger.exception('Games Exception : '+str(e))
    return HttpResponse('')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').count() != 0)
def highscores(request,gamecode):
  try:
    games = CanvasGame.registered_games
    game = games[gamecode]
    gamescores = GameScore.objects.filter(gamecode=gamecode).order_by('-score')[:10]
    return render_to_response('games/highscores.html',{'games':games,'game':game,'gamescores':gamescores
        },context_instance=RequestContext(request))
  except Exception as e:
    logger.exception('Games Exception : '+str(e))
    messages.error(request, 'Unknown error has occured. Please try again later. The issue has beeen reported')
    return render_to_response('error.html', {
        }, context_instance=RequestContext(request))

