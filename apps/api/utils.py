import json
from functools import wraps

from django.http import HttpResponse
from django.shortcuts import render

def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  return ip

def int2roman(number):
  numerals = { 1 : "I", 4 : "IV", 5 : "V", 9 : "IX", 10 : "X", 40 : "XL",
    50 : "L", 90 : "XC", 100 : "C", 400 : "CD", 500 : "D", 900 : "CM", 1000 : "M" }
  result = ""
  for value, numeral in sorted(numerals.items(), reverse=True):
    while number >= value:
      result += numeral
      number -= value
  return result

def pagelet_login_required(view):
  @wraps(view)
  def wrapped_view(request, *args, **kwargs):
    if request.user.is_authenticated():
      return view(request, *args, **kwargs)
    else:
      return render(request, 'pagelet_base.html')
  return wrapped_view

def dialog_login_required(view):
  @wraps(view)
  def wrapped_view(request, *args, **kwargs):
    if request.user.is_authenticated():
      return view(request, *args, **kwargs)
    else:
      return render(request, 'dialog_base.html')
  return wrapped_view

def dialog_login_required_buyandsell(view):
  @wraps(view)
  def wrapped_view(request, *args, **kwargs):
    if request.user.is_authenticated():
      return view(request, *args, **kwargs)
    else:
      return render(request, 'dialog_base_buyandsell.html')
  return wrapped_view

def ajax_login_required(view):
  @wraps(view)
  def wrapped_view(request, *args, **kwargs):
    if request.user.is_authenticated():
      return view(request, *args, **kwargs)
    else:
      return HttpResponse(json.dumps({}), content_type='application/json')
  return wrapped_view

def escape_with_quotes(value):
  if not isinstance(value, basestring):
    value = str(value)
  return '"%s"'%(value.replace("\\","\\\\").replace(r'"',r'\"'))
