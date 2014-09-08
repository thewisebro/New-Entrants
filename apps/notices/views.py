import os
from BeautifulSoup import BeautifulSoup

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from notices.serializer import *
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.views.generic import TemplateView
import simplejson
from django.conf import settings

from filemanager import FileManager
from notices.models import *
from notices.forms import *
from notices.utils import *

privelege=0
PeopleProxyUrl = "http://people.iitr.ernet.in/"

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
  category = None
  categories = request.user.category_set.all()
  form = DummyForm()
  if (privelege and request.method == 'POST' and request.POST.has_key('category_name') and request.POST['category_name']):
    category = Category.objects.get(name = request.POST['category_name'])
    NoticeForm = GenerateNoticeForm(category)
    if request.POST.has_key('Submit'):
      form = NoticeForm(request.POST)
      if form.is_valid():
        uploader = Uploader.objects.get(user=request.user, category=category)
        notice = form.save(commit=False)
        notice.content = html_parsing_while_uploading(notice.content)
        notice.uploader = uploader
        notice.save()
        return HttpResponseRedirect('/#notices')
    else:
      form =  NoticeForm()
  context = {'category' : category, 'categories' : categories, 'form' : form, 'privelege' : privelege}
  return render(request, 'notices/upload.html', context)

class PrivelegeJsonView(TemplateView):
  def get(self, request):
    global privelege
    privelege = request.user.uploader_set.all().exists()
    privelege1 = {'privelege' : privelege}
    privelege_json = simplejson.dumps(privelege1)
    return HttpResponse(privelege_json, mimetype="application/json")

class GetConstants(TemplateView):
  def get(self, request):
    constants_list = simplejson.dumps(MAIN_CATEGORIES)
    return HttpResponse(constants_list, mimetype="application/json")

class NoticeListView(ListAPIView):
  serializer_class = NoticeListViewSerializer
  def get_queryset(self):
    mode = self.kwargs['mode']
    if(mode=="old"):
      queryset = Notice.objects.filter(expired_status=True)
    else:
      queryset = Notice.objects.filter(expired_status=False)
    mc = self.kwargs['mc']
    subc = self.kwargs['subc']
    llim = int(self.kwargs['llim'])                                #lower limit
    hlim = int(self.kwargs['hlim'])                                #higher limit
    first_notice_id = int(self.kwargs['id'])                       #id of the first notice relative to which the number of notices to be sent is realized
    a = 0
    count = 0
    temp = 0
    if first_notice_id!=0:
      while temp==0:
        if(mc=="All"):
          query = queryset.order_by('-datetime_modified')[a:a+10]
        elif(subc=="All"):
          query = queryset.filter(uploader__category__main_category=mc).order_by('-datetime_modified')[a:a+10]
        else:
          query = queryset.filter(uploader__category__name=subc).order_by('-datetime_modified')[a:a+10]
        for x in query:
          if x.id==first_notice_id:
            temp=1
            break
          count += 1
        a += 10
    llim = llim + count
    hlim = hlim + count + 1
    if(mc=="All"):
      queryset = queryset.order_by('-datetime_modified')[llim:hlim]
    elif(subc=="All"):
       queryset = queryset.filter(uploader__category__main_category=mc).order_by('-datetime_modified')[llim:hlim]
    else:
       queryset = queryset.filter(uploader__category__name=subc).order_by('-datetime_modified')[llim:hlim]
    return queryset

class Maxnumber(TemplateView):
  def get(self, request):
    number_json = simplejson.dumps({'total_new_notices' : len(Notice.objects.filter(expired_status=False)),'total_old_notices' : len(Notice.objects.filter(expired_status=True)) })
    return HttpResponse(number_json, mimetype="application/json")

class TempMaxNotice(TemplateView):
  def get(self, request, mode, mc, subc):
    if(mode=="new"):
      queryset = Notice.objects.filter(expired_status=False)
    else:
      queryset = Notice.objects.filter(expired_status=True)
    if(subc=="All"):
      number_json = simplejson.dumps({'total_notices' : len(queryset.filter(uploader__category__main_category=mc))})
    else:
      number_json = simplejson.dumps({'total_notices' : len(queryset.filter(uploader__category__name=subc))})
    return HttpResponse(number_json, mimetype="application/json")

class GetNotice(RetrieveAPIView):
  queryset = Notice.objects.all()
  serializer_class = GetNoticeSerializer

class NoticeSearch(ListAPIView):
  def get_queryset(self):
    queryset = []
    query = self.request.GET.get('q', '')
    mode = self.kwargs['mode']
    if(mode=="old"):
      queryset1 = Notice.objects.filter(expired_status=True)
    else:
      queryset1 = Notice.objects.filter(expired_status=False)
    mc = self.kwargs['mc']
    subc = self.kwargs['subc']
    if(subc=="All" and mc=="All"):
      query1=queryset1
    elif(subc=="All"):
      query1=queryset1.filter(uploader__category__main_category=mc)
    else:
      query1=queryset1.filter(uploader__category__name=subc)

    if query[:2]==">>":
      print "abcd"
      query=query[2:].split("-")
      queryset = query1.filter(datetime_modified__gt=datetime.fromtimestamp(int(query[0])/1000.0)).filter(datetime_modified__lt=datetime.fromtimestamp(int(query[1])/1000.0))

    else:
      words = query.split(' ')
      un_queryset = {}			#unsorted(with respect to frequency) queryset
      count = {}
      for word in words:
        result = query1.filter(Q(subject__icontains=word) | Q(content__icontains=word))
        for temp in result:
          print word
          if temp.id in un_queryset:
            count[temp.id] = count[temp.id]+1
          else:
            un_queryset[temp.id] = temp
            count[temp.id] = 1
      date_sorted_queryset=sorted(un_queryset, key= lambda l : un_queryset[l].datetime_modified, reverse=True)
      count_date_sorted_queryset=sorted(date_sorted_queryset, key= lambda l: count[l], reverse=True)
      for notice_id in count_date_sorted_queryset:
        queryset.append(un_queryset[notice_id])
    return queryset
  serializer_class = GetNoticeSerializer

@login_required
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

@login_required
def mul_read_star_notice(request, action):              #action determines whether the function of this view is to star, unstar, read or unread a notice
  user1 = request.user
  notice_user = NoticeUser.objects.get(user=user1)
  list1 = request.GET.get('q', '')
  ids = list1.split(' ')
  for i in ids:
    notice_temp = Notice.objects.get(id=i)
    if action=="add_starred":
      notice_user.starred_notices.add(notice_temp)
    elif action=="add_read":
      notice_user.read_notices.add(notice_temp)
    elif action=="delete_starred":
		  notice_user.starred_notices.remove(notice_temp)
    else:
		  notice_user.read_notices.remove(notice_temp)
  success = {'success' : 'true'}
  success = simplejson.dumps(success)
  return HttpResponse(success, mimetype="application/json")

class Show_Starred(ListAPIView):
  def get_queryset(self):
    user = NoticeUser.objects.get(user=self.request.user)
    queryset = user.starred_notices.all().order_by('-datetime_modified')
    return queryset
  serializer_class = NoticeListViewSerializer

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
    if privelege:
      uploaders = self.request.user.uploader_set.all()
      for i in uploaders:
        queryset += i.notice_set.all().order_by('-datetime_modified')
    return queryset
  serializer_class = NoticeListViewSerializer

@login_required
def edit(request, pk):
  NoticeForm = EditForm()
  n = Notice.objects.get(id=pk)
  if request.method == 'POST' and privelege:
    form = EditForm(request.POST)
    if form.is_valid():
      if n.datetime_modified==n.datetime_created:
        tnotice = TrashNotice(subject=n.subject, reference=n.reference, expire_date=n.expire_date, content=n.content, uploader=n.uploader, emailsend=n.emailsend, re_edited=n.re_edited, expired_status=n.expired_status, notice_id=n.pk, editing_no=1, datetime_created=n.datetime_modified, original_datetime = n.datetime_created)
      else:
        new_edit_no = max(map(lambda a:a.editing_no,TrashNotice.objects.filter(notice_id=n.pk)))+1
        tnotice = TrashNotice(subject=n.subject, reference=n.reference, expire_date=n.expire_date, content=n.content, uploader=n.uploader, emailsend=n.emailsend, re_edited=n.re_edited, expired_status=n.expired_status, notice_id=n.pk, editing_no = new_edit_no, datetime_created=n.datetime_modified, original_datetime = n.datetime_created)
      notice = form.save(commit=False)
      n.subject = notice.subject
      n.reference = notice.reference
      n.content = html_parsing_while_uploading(notice.content)
      n.expire_date = notice.expire_date
      for user in n.read_noticeuser_set.all():
        n.read_noticeuser_set.remove(user)
      n.re_edited = True
      n.save()
      tnotice.datetime_created=n.datetime_modified
      tnotice.save()
      return HttpResponseRedirect('/#notices')
  else:
    print n.content
    print "abc"
    print remove_pdfimages
    form =  EditForm(
              initial={'subject' : n.subject, 'reference' : n.reference , 'expire_date' : n.expire_date , 'content' : remove_pdfimages(n.content), 'category' : n.uploader.category.name})
  context = {'form' : form, 'privelege' : privelege, 'category' : n.uploader.category.name}
  return render(request, 'notices/edit.html', context)

@login_required
def delete(request, pk):
  n = Notice.objects.get(id=pk)
  if privelege:
    tnotice = TrashNotice(subject=n.subject, reference=n.reference, expire_date=n.expire_date, content=n.content, uploader=n.uploader, emailsend=n.emailsend, re_edited=n.re_edited, expired_status=n.expired_status, notice_id=n.pk, editing_no=-1, datetime_created=n.datetime_modified, original_datetime = n.datetime_created)
    tnotice.save()
    n.delete()
  return HttpResponseRedirect('/#notices')

@login_required
def browse(request,category_name,path):
  print "abc"
  category = Category.objects.get(name = category_name)
  if request.user in category.users.all():
    if not os.path.exists(settings.MEDIA_ROOT+'notices/uploads/'+category.name):
      os.chdir(settings.MEDIA_ROOT+'notices/uploads/')
      os.mkdir(category.name)
    fm = FileManager(basepath=settings.MEDIA_ROOT+'notices/uploads/'+category.name,
        ckeditor_baseurl='/media/notices/uploads/'+category.name,
        maxspace=50*1024, maxfilesize=5*1024)
    return fm.render(request,path)

"""class Star_notice_list(TemplateView):
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
"""

