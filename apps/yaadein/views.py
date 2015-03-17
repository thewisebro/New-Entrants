from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from yaadein.models import Post,PostImage,YaadeinUser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from taggit.models import Tag,TaggedItem
from django.views.generic import DetailView, ListView
from nucleus.models import Student,User
from django.db.models import Q,Count
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from notifications.models import Notification
#from nucleus import get_info, html_name
import json as simplejson
"""
def CORS_allow(view):
  def wrapped_view(request, *args, **kwargs):
    if settings.PRODUCTION:
      return view(request, *args, **kwargs)
    else:
      response = (csrf_exempt(view))(request, *args, **kwargs)
      response["Access-Control-Allow-Origin"] = "http://172.25.55.156:7000"
      response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT"
      response["Access-Control-Allow-Credentials"] = True
#     response["Access-Control-Max-Age"] = "1000"
      response["Access-Control-Allow-Headers"] = "accept, content-type"
    return response
  return wrapped_view
"""

def CORS_allow(view):
  def wrapped_view(request, *args, **kwargs):
    response = view(request, *args, **kwargs)
    if settings.PRODUCTION == False:
      response["Access-Control-Allow-Origin"] = "*"
      response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
      response["Access-Control-Allow-Credentials"] = True
#     response["Access-Control-Max-Age"] = "1000"
      response["Access-Control-Allow-Headers"] = "*"
    return response
  return wrapped_view

@csrf_exempt
@CORS_allow
#@login_required
def index(request,enrno=None):
# import ipdb;ipdb.set_trace()
  if request.method == 'GET':
    y_user = YaadeinUser.objects.get_or_create(user__username='13117060')[0]#user=request.user
    logged_user = y_user.user
#user = User.objects.get(username ='13114068')
#  if y_user.coverpic.field.blank :
#    y_user.coverpic = "yaadein/coverpic/image4.jpg"
    s = Student.objects.get(user__username=enrno)#=enrno
#    posts = s.post_wall_user.order_by('post_date').reverse()
    posts_usertagged = Post.objects.filter(user_tags=s)#s.tagged_user.order_by('post_date').reverse() #posts in which user is tagged
    posts_owned = Post.objects.filter(owner=s)
    posts_onwall = Post.objects.filter(wall_user=s)
    posts = list(set(list(posts_onwall)+list(posts_owned)+list(posts_usertagged)))#.order_by('post_date').reverse()
    bubble(posts)
    posts_data = []
    for post in posts:
        images = PostImage.objects.filter(post=post)
        image_url=[]
        users_tagged_inpost = []
        users = post.user_tags.all()
        for image in images:
          image_url.append(image.image.url)
        if len(users)>0:
          for user in users:
            users_tagged_inpost.append({'name':user.user.name,'username':user.user.username,})
        tmp = {
               'post_text': post.text_content,
               'post_owner':post.owner.user.name,
               'post_owner_branch':post.owner.user.info,
               'post_owner_pic':post.owner.user.photo_url,
               'post_owner_enrol':post.owner.user.username,
               'post_id':str(post.pk),
               'image_url': image_url,
               'time':str(post.post_date),
               'wall_user':post.wall_user.user.name,
               'wall_user_enrol':post.wall_user.user.username,
               'taggedUsers':users_tagged_inpost,
               }
        posts_data.append( tmp )
    data ={'name':logged_user.name, 'coverPic': y_user.coverpic.url, 'enrolmentNo':enrno, 'posts_data':posts_data, 'label':logged_user.info, 'profilePic':logged_user.photo_url}
    return HttpResponse(simplejson.dumps(data),'application/json') 
#  return render_to_response('yaadein/usertag.html', {'cover_pic': y_user.coverpic.url,'enrno':enrno,'posts_data':posts_data}, context_instance=RequestContext(request))
  else:
#  import ipdb;ipdb.set_trace()
    print 'vaibhavraj'
    if request.method == 'POST':
      post_data = str(simplejson.loads(request.POST['data'])['post_text'])
      user_tagged = simplejson.loads(request.POST['data'])['user_tags']
      hashed = [ word for word in post_data.split() if word.startswith("#") ]
      hash_tag = []
      for word in hashed:
# temp =[ word.split('#') ]
        temp =  filter(None, word.replace(' ','').split("#"))
        hash_tag.extend(temp)
      hash_tag = list(set(hash_tag))
      for i in range(0,len(hash_tag)):
        hash_tag[i] = '#'+hash_tag[i]
#user_tagged = [ tag for tag in post_data.split() if tag.startswith("@") ]
      imgs = request.FILES.getlist('file')
      print len(imgs)
      student = Student.objects.get(user__username="13117060")
      if enrno:#wall_user:
        s = Student.objects.get(user__username=enrno)#wall_user)
        post = Post(text_content=post_data, post_date=timezone.now(), owner=student, wall_user=s)
      else:
        post = Post(text_content=post_data, post_date=timezone.now(), owner=student)
      post.save()
      notif_msg = 'You were tagged in a memory by '+student.user.name+'.'
      notif_msg1 = ''+student.user.name+' posted a memory on your wall'  
      app = 'Yaadein'
      pk = str(post.pk)
      url = '/yaadein/post_disp/'+pk+'/'
      notif_users=[]
      tagged_users = []
      if enrno!='13114068':
        notif_users.append(s.user)
        Notification.save_notification(app,notif_msg1,url,notif_users,post)
      print post.wall_user
      if len(imgs)>0:
        for key in imgs:
          PI = PostImage(image = key,post = post)
          PI.save()
      for hash in hash_tag:
        print hash
        post.tags.add(hash)
      for user in user_tagged:
#      user = user[1:]
        student_related = Student.objects.get(user__username=str(user['id']))
        tagged_users.append(student_related.user)
        post.user_tags.add(student_related)
      if len(user_tagged)>0: 
        Notification.save_notification(app,notif_msg,url,tagged_users,post)  
      data = {'temp':"a"}
# return  HttpResponse("post added")
      return HttpResponse(simplejson.dumps(data),'application/json')
    else:
      return HttpResponse('Hello')

@csrf_exempt
@CORS_allow
def homePage(request):
#  import ipdb;ipdb.set_trace()
  y_user = YaadeinUser.objects.get_or_create(user__username='13117060')[0]#user=request.user
  logged_user = y_user.user
  s = Student.objects.get(user__username='13117060')#=enrno
  posts = Post.objects.order_by('post_date').filter(status= 'A').reverse()
  posts_data = []
  for post in posts:
      images = PostImage.objects.filter(post=post)
      image_url=[]
      for image in images:
        image_url.append(image.image.url)
      tmp = {
             'post_text': post.text_content,
             'post_owner':post.owner.user.name,
             'post_owner_branch':post.owner.user.info,
             'post_owner_pic':post.owner.user.photo_url,
             'post_owner_enrol':post.owner.user.username,
             'post_id':str(post.pk),
             'image_url': image_url,
             'time':str(post.post_date)
             }
      posts_data.append( tmp )
  data ={'name':logged_user.name, 'coverPic': y_user.coverpic.url, 'enrolmentNo':logged_user.username, 'posts_data':posts_data, 'label':logged_user.info, 'profilePic':logged_user.photo_url}
  return HttpResponse(simplejson.dumps(data),'application/json') 


@csrf_exempt
@CORS_allow
#@login_required
def coverpic_upload(request):
# import ipdb;ipdb.set_trace()
  if request.method == 'POST': #and request.is_ajax():
    cover_pic = request.FILES.get('file')
    print cover_pic
    cover_pic_name = cover_pic.name
    ext = cover_pic.name.split('.')[1]
    fname = "cp_" + request.user.username + "." + ext
    yu = YaadeinUser.objects.get(user__username = '13117060')#request.user)
    yu.coverpic.save(fname, cover_pic)
    yu.save()
    return HttpResponse('Uploaded')#/yaadein/user/13117060')
  else:
    return HttpResponse('hello')
#  return render_to_response('yaadein/base.html',{},context_instance=requestContext(request))

@csrf_exempt
@CORS_allow
def post(request,wall_user):
# import ipdb;ipdb.set_trace()
  if request:
    print 'vaibhavraj'
    if request.method == 'POST':
      post_data = str(simplejson.loads(request.POST['data'])['post_text'])
      hashed = [ word for word in post_data.split() if word.startswith("#") ]
      hash_tag = []
      for word in hashed:
# te mp =[ word.split('#') ]
        temp =  filter(None, word.replace(' ','').split("#"))
        hash_tag.extend(temp)
      hash_tag = list(set(hash_tag))
      for i in range(0,len(hash_tag)):
        hash_tag[i] = '#'+hash_tag[i] 
      user_tagged = [ tag for tag in post_data.split() if tag.startswith("@") ]
      imgs = request.FILES.getlist('file')
      print len(imgs)
      print wall_user
      if wall_user:
        s = Student.objects.get(user__username=wall_user)
      else:
        s = Student.objects.get(user__username="13117060")
      print s
      student = Student.objects.get(user__username="13117060")
      post = Post(text_content=post_data, post_date=timezone.now(), owner=student, wall_user=s)
      post.save()
# notif_msg = 'You were tagged in a post by '+student.user.name+'.'
#     app = 'Yaadein'
#     pk = post.pk
#     url = '/yaadein/post_disp/'+pk+'/'  
#     Notification.save_notification(app,notif_msg,url,user_tagged,post)
      print post.wall_user
      if len(imgs)>0:
        for key in imgs:
          PI = PostImage(image = key,post = post)
          PI.save()
      for hash in hash_tag:
        print hash
        post.tags.add(hash)
      for user in user_tagged:
        user = user[1:]
        student_related = Student.objects.get(user__name=user)
        post.user_tags.add(student_related)
      data = {'temp':"a"}
# return  HttpResponse("post added")
      return HttpResponse(simplejson.dumps(data),'application/json')
    else:
      return HttpResponse('Hello')


#view to display a single post
@csrf_exempt
@CORS_allow
def post_display(request,pk):
  if request:
    post = Post.objects.get(pk=pk)
    images = PostImage.objects.filter(post=post)
    image_url=[]
    for image in images:
      image_url.append(image.image.url)
    data = {
             'post_text': post.text_content,
             'post_owner':post.owner.user.name,
             'post_owner_branch':post.owner.user.info,
             'post_owner_pic':post.owner.user.photo_url,
             'post_owner_enrol':post.owner.user.username,
             'image_url': image_url,
             'time':str(post.post_date)
             }
    return HttpResponse(simplejson.dumps(data),'application/json')
  else:
    return HttpResponse('Hello')

@CORS_allow
def person_search(request):
   if request: #.is_ajax():
     query = request.GET.get('q','')
# import ipdb;ipdb.set_trace()
     students = Student.objects.filter(Q(user__name__icontains = query)).order_by('-user__name')[:10]
     def person_dict(student):
       return {
         'id':student.user.username,
         'label':student.user.info,
         'value':student.user.name,
         'profile_pic':student.user.photo_url
        }
     data = map(person_dict,students)
     search_data = {'results':data}
   else:
     data = 'fail'
   return HttpResponse(simplejson.dumps(search_data),'application/json')

@csrf_exempt
@CORS_allow
def hashtag(request,slug):
  if request:
    posts_data = []
    posts = Post.objects.filter(tags__slug=slug).order_by('post_date').reverse()  
    for post in posts:
          images = PostImage.objects.filter(post=post)
          image_url=[]
          for image in images:
            image_url.append(image.image.url)
          tmp = {
             'post_text': post.text_content,
             'post_owner':post.owner.user.name,
             'post_owner_branch':post.owner.user.info,
             'post_owner_pic':post.owner.user.photo_url,
             'post_owner_enrol':post.owner.user.username,
             'image_url': image_url,
             'time':str(post.post_date)
             }
          posts_data.append( tmp )
    data ={'posts_data':posts_data}
    return HttpResponse(simplejson.dumps(data),'application/json')
  return HttpResponse('1')

@csrf_exempt
@CORS_allow
def delete(request,id):
  if request:
    try:
      post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
      return HttpResponse("Post Doesnot exist")
    if post.owner.user.username=='13114068' or post.wall_user.user.username=='13117060': #use request.user in place of enrollment number
      post.delete()
      return HttpResponse("Post deleted Successfully.")
    return HttpResponse("you don't have the previleges to delete this post.")

@csrf_exempt
@CORS_allow
def private_posts(request,id):
  if request:
    try:
      post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
      return HttpResponse("Post Doesnot Exist")
    if post.owner.username=='13114068' or post.wall_user.user.username=='13117060':
      post.status = 'B'
      post.save()
      return HttpResponse("Your Post is now Private.")
    return HttpResponse("You don't have the previleges to change the privacy.")

def trending(request):
  trending_users =  Student.objects.filter(tagged_user__in=posts).annotate(itemCount=Count('tagged_user')).order_by('-itemCount')
  user_list=[]
  for tr in trending_users:
    temp={
          'name':tr.user.username,
          'enrno':tr.user.name,
        }
    user_list.append(temp)
  data = {'user_list':user_list}
  return HttpResponse(simplejson.dumps(data),'application/json')

  
#utility function bubble sorting
def bubble(bad_list):
  length = len(bad_list) - 1
  sorted = False

  while not sorted:
    sorted = True
    for i in range(length):
      if bad_list[i].post_date < bad_list[i+1].post_date:
        sorted = False
        bad_list[i], bad_list[i+1] = bad_list[i+1], bad_list[i]
  return bad_list    
  """
class TagIndexView(ListView):
# template_name = 'yaadein/tagged.html'
# model = Post
#      context_object_name = 'posts_data'

      @CORS_allow
      @csrf_exempt
#     def get_queryset(self):
      def get_context_data(self, **kwargs):
#   import ipdb;ipdb.set_trace()
        context = super(TagIndexView, self).get_context_data(**kwargs)
        posts_data = []
        posts = Post.objects.filter(tags__slug=self.kwargs.get('slug')).reverse()
        for post in posts:
          images = PostImage.objects.filter(post=post)
          image_url=[]
          for image in images:
            image_url.append(image.image.url)
          tmp = {
             'post_text': post.text_content,
             'post_owner':post.owner.user.name,
             'post_owner_branch':post.owner.user.info,
             'post_owner_pic':post.owner.user.photo_url,
             'post_owner_enrol':post.owner.user.username,
             'image_url': image_url,
             'time':str(post.post_date)
             }
          posts_data.append( tmp )
#  data ={'posts_data':posts_data}
          context['posts_data'] = posts_data
        return context
# return HttpResponse(simplejson.dumps(context['posts_data']),'application/json')

"""
"""
class tag_user(ListView):
     template_name='yaadein/usertag.html'
     model = Post
     context_object_name = 'posts'

     def get_queryset(self):
       s = Student.objects.get(user__username=self.kwargs.get('enrno'))
       return s.post_wall_user.all()
"""
