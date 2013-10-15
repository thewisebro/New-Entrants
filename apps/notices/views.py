from django.contrib.auth.models import User
from django.shortcuts import render
from notices.forms import *
from django.http import HttpResponseRedirect, HttpResponse
from notices.models import *
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from notices.serializer import *

from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.views.generic import TemplateView
import simplejson

def index(request):
  user = request.user
  notice_list = Notice.objects.order_by('datetime_modified')[0:10]
  if user.is_authenticated():
    privelege = user.uploader_set.all().exists()
    context = {'privelege' : privelege, 'notice_list' : notice_list }
    return render(request, 'notices/notice_list.html', context)
  context = { 'notice_list' : notice_list }
  return render(request, 'notices/notice_list.html', context)

@login_required
def upload(request):
  NoticeForm = GenerateNoticeForm(request.user)
  privelege = request.user.uploader_set.all().exists()
  if request.method == 'POST' :
    form = NoticeForm(request.POST)
    if form.is_valid():
      c=Category.objects.get(name=form.cleaned_data['category'])
      uploader = Uploader.objects.get(user=request.user, category=c)
      notice = form.save(commit=False)
      notice.uploader = uploader
      notice.save()
      return HttpResponseRedirect(reverse('index'))
  else:
    form =  NoticeForm()
  context = {'form' : form, 'privelege' : privelege}
  return render(request, 'notices/upload.html', context)

class PrivelegeJsonView(TemplateView):
  def get(self, request):
    privelege = request.user.uploader_set.all().exists()
    privelege = {'privelege' : privelege}
    privelege_json = simplejson.dumps(privelege)
    return HttpResponse(privelege_json, mimetype="application/json")

class NoticeListView(ListAPIView):
  serializer_class = NoticeListViewSerializer
  def get_queryset(self):
    page_no = int(self.kwargs['page_no'])
    a = page_no*10
    b = a - 10
    return Notice.objects.order_by('datetime_modified')[b:a]

class Maxnumber(TemplateView):
  def get(self, request):
    number_json = simplejson.dumps({'total_notices' : len(Notice.objects.all()) })
    return HttpResponse(number_json, mimetype="application/json")

class GetNotice(RetrieveAPIView):
  queryset = Notice.objects.all()
  serializer_class = GetNoticeSerializer


