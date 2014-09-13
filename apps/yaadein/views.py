from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response



def index(request):
  return render_to_response('yaadein/base.html',{},context_instance=RequestContext(request))

