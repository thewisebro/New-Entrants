from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from yaadein.models import post
from django.shortcuts import get_object_or_404
from django.utils import timezone

def index(request):
  if request.method == 'POST':
    p = request.POST['content']
    Post = post(text_content=p,post_date=timezone.now())
    Post.save()
    return  HttpResponse("post added")

  return render_to_response('yaadein/base.html',{},context_instance=RequestContext(request))



