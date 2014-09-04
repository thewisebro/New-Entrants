from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from nucleus.models import User, Student, Connection, FriendRequest

import json
import logging
logger = logging.getLogger('channel-i_logger')

import redis
client = redis.Redis("localhost")

def send_friend_request(request):
  to_user_id = request.POST.get('to_user_id')
  to_user = User.objects.get(pk=to_user_id)
  from_user = request.user
  if to_user is None and from_user is None:
    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    fr_data = {'from_user':from_user.name, 'to_user': to_user.name}
    json_data = json.dumps(fr_data)
    return HttpResponse(json_data, content_type='application/json')
  return HttpResponse('', content_type='application/json')

@login_required
def respond_to_friend_request(request):
  to_user_id = request.POST.get('to_user_id')
  to_user = User.objects.get(pk=to_user_id)
  status = request.POST.get('status')
  from_user = request.user
  if from_user is not None and to_user is not None and status is not None:
    if status is 'Accepted':
      from_user.add_connection(to_user)
      #from_user__user_info = {'name': from_user.name, 'enr': from_user.username, 'status': 0, 'is_chat_on': 0}
      #to_user__user_info = {'name': to_user.name, 'enr': to_user.username, 'status': 0, 'is_chat_on': 0}
      #client.hmset('user:'+from_user.username, from_user__user_info)
      #client.hmset('user:'+to_user.username, to_user__user_info)
      #client.sadd('friends:'+from_user.username, to_user.username)
      FriendRequest.objects.get(from_user = from_user, to_user=to_user).delete()
      conn_data = {'from_user': from_user.name, 'to_user': to_user.name, 'status': 'Accepted'}
      json_data = json.dumps(conn_data)
      return HttpResponse(json_data, content_type='application/json')

    elif status is 'Declined':
      fr = FriendRequest.objects.get(from_user = from_user, to_user=to_user)
      fr.is_declined = True
      fr.save()
      fr_data = {'from_user': from_user.name, 'to_user': to_user.name, 'status': 'Declined'}
      json_data = json.dumps(fr_data)
      return HttpResponse(json_data, content_type='application/json')
    else:
      return HttpResponse("")
  else:
    return HttpResponse("")

@login_required
def unfriend_connection(request):
  to_user_id = request.POST.get('to_user_id')
  to_user = User.objects.get(pk=to_user_id)
  from_user = request.user
  if from_user is not None and to_user is not None:
    from_user.remove_connection(to_user) # UNFRIEND
    #client.srem('friends:'+from_user.username, to_user.username)
    conn_data = {'from_user': from_user.name, 'to_user': to_user.name, 'status': 'UNFRIEND'}
    json_data = json.dumps(conn_data)
    return HttpResponse(json_data, content_type='application/json')
  return HttpResponse('')

@login_required
def block_connection(request):
  to_user_id = request.POST.get('to_user_id')
  to_user = User.objects.get(pk=to_user_id)
  from_user = request.user
  if from_user is not None and to_user is not None:
    from_user.update_connection(to_user, 3) # Block Friend
    #client.srem('friends:'+from_user.username, to_user.username)
    conn_data = {'from_user': from_user.name, 'to_user': to_user.name, 'status': 'Blocked'}
    json_data = json.dumps(conn_data)
    return HttpResponse(json_data, content_type='application/json')
  return HttpResponse('')

@login_required
def fetch_friend_requests(request):
  from_user = request.user
  friend_requests = FriendRequests.objects.filter(from_user=from_user, is_declined=False)
  fr_data = []
  for fr in friend_requets:
    tmp = {'from_user':from_user.name, 'to_user': fr.to_user.name, 'is_seen': fr.is_seen}
    fr_data.append[tmp]
  json_data = json.dumps(fr_data)
  return HttpResponse(json_data, content_type='application/json')

