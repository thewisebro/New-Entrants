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
  if request.method == 'POST' and privelege:
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
    llim = int(self.kwargs['llim'])                                #lower limit
    hlim = int(self.kwargs['hlim'])                                #higher limit
    first_notice_id = int(self.kwargs['id'])                       #id of the first notice relative to which the number of notices to be sent are realized
    a = 0
    count = 0
    temp = 0
    if first_notice_id!=0:
      while temp==0:
        query = Notice.objects.order_by('-datetime_modified')[a:a+10]
        for x in query:
          if x.id==first_notice_id:
            temp=1
            break
          count += 1
        a += 10
    llim = llim + count
    hlim = hlim + count + 1
    queryset = Notice.objects.order_by('-datetime_modified')[llim:hlim]
    return queryset

class Maxnumber(TemplateView):
  def get(self, request):
    number_json = simplejson.dumps({'total_notices' : len(Notice.objects.all()) })
    return HttpResponse(number_json, mimetype="application/json")

class GetNotice(RetrieveAPIView):
  queryset = Notice.objects.all()
  serializer_class = GetNoticeSerializer


class NoticeSearch(ListAPIView):
  def get_queryset(self):
	query = self.request.GET.get('q', '')
	print query
	words = query.split(' ')
	un_queryset = {}			#unsorted(with respect to frequency) queryset
	count = {}
	for word in words:
		result = Notice.objects.filter(subject__icontains=word)
		for temp in result:
			if temp.id in un_queryset:
				count[temp.id] = count[temp.id]+1
			else:
				un_queryset[temp.id] = temp
				count[temp.id] = 1
	date_sorted_queryset=sorted(un_queryset, key= lambda l : un_queryset[l].datetime_modified, reverse=True)
	count_date_sorted_queryset=sorted(date_sorted_queryset, key= lambda l: count[l], reverse=True)
	queryset = []				#Sorted queryset
	for notice_id in count_date_sorted_queryset:
		queryset.append(un_queryset[notice_id])
	return queryset
  serializer_class = GetNoticeSerializer

def read_star_notice(request, id1, action):              #action determines whether the function of this view is to star, unstar, read or unread a notice
  user1 = request.user
  notice_user = NoticeUser.objects.get(user=user1)
  notice_temp = Notice.objects.get(id=id1)
  if action=="add_starred":
    notice_user.starred_notices.add(notice_temp)
  elif action=="add_read":
    notice_user.read_notices.add(notice_temp)
  else:
		notice_user.starred_notices.remove(notice_temp)
  success = {'success' : 'true'}
  success = simplejson.dumps(success)
  return HttpResponse(success, mimetype="application/json")

class Star_notice_list(TemplateView):
  def get(self, request):
    user = NoticeUser.objects.get(user=request.user)
    notices = user.starred_notices.all().order_by('-datetime_modified')
    dictionary = {}
    t=0
    for i in notices:
      dictionary[t] = i.id
      t=t+1
    d_json = simplejson.dumps(dictionary)
    return HttpResponse(d_json, mimetype="application/json")

class Read_notice_list(TemplateView):
  def get(self, request):
    user = NoticeUser.objects.get(user=request.user)
    notices = user.read_notices.all().order_by('-datetime_modified')
    dictionary = {}
    t=0
    for i in notices:
      dictionary[t] = i.id
      t=t+1
    d_json = simplejson.dumps(dictionary)
    return HttpResponse(d_json, mimetype="application/json")

class Show_Uploads(ListAPIView):
  def get_queryset(self):
    queryset = []
    uploaders = self.request.user.uploader_set.all()
    for i in uploaders:
      queryset += i.notice_set.all().order_by('-datetime_modified')
    return queryset
  serializer_class = NoticeListViewSerializer

@login_required
def edit(request, pk):
  NoticeForm = GenerateNoticeForm(request.user)
  privelege = request.user.uploader_set.all().exists()
  notice = Notice.objects.get(id=pk)
  if request.method == 'POST' and privelege:
    form = NoticeForm(request.POST)
    if form.is_valid():

      c=Category.objects.get(name=form.cleaned_data['category'])
      uploader = Uploader.objects.get(user=request.user, category=c)
      notice = form.save(commit=False)
      notice.uploader = uploader
      notice.re_edited = True
      notice.save()
      return HttpResponseRedirect(reverse('index'))
  else:
    form =  NoticeForm(
              initial={'subject' : notice.subject, 'reference' : notice.reference , 'expire_date' : notice.expire_date , 'content' : notice.content, 'category' : notice.uploader.category})
  context = {'form' : form, 'privelege' : privelege}
  return render(request, 'notices/upload.html', context)
