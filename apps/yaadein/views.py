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
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
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
  y_user = YaadeinUser.objects.get_or_create(user__username='13114068')[0]#user=request.user
  logged_user = y_user.user
#user = User.objects.get(username ='13114068')
  s = Student.objects.get(user__username='13114068')#=enrno
  posts = s.post_wall_user.all()
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
             'image_url': image_url,
             'time':str(datetime.now()),

             }
      posts_data.append( tmp )
  data ={'name':logged_user.name, 'coverPic': y_user.coverpic.url, 'enrolmentNo':enrno, 'posts_data':posts_data, 'label':logged_user.info, 'profilePic':logged_user.photo_url}
  return HttpResponse(simplejson.dumps(data),'application/json') 
#  return render_to_response('yaadein/usertag.html', {'cover_pic': y_user.coverpic.url,'enrno':enrno,'posts_data':posts_data}, context_instance=RequestContext(request))

@csrf_exempt
@CORS_allow
#@login_required
def coverpic_upload(request):
  if request.method == 'POST': #and request.is_ajax():
    cover_pic = request.FILES.get('cover')
    print cover_pic
    cover_pic_name = cover_pic.name
    ext = cover_pic.name.split('.')[1]
    fname = "cp_" + request.user.username + "." + ext
    yu = YaadeinUser.objects.get(user = request.user)
    yu.coverpic.save(fname, cover_pic)
    yu.save()
  return HttpResponseRedirect('/yaadein/')
#  return render_to_response('yaadein/base.html',{},context_instance=requestContext(request))

@csrf_exempt
@CORS_allow
def post(request,wall_user):
  import ipdb;ipdb.set_trace()
  if request:
      print 'vaibhavraj'
      if request.method == 'POST':
        p = request.POST.get('post_text')
        hashed = [ word for word in p.split() if word.startswith("#") ]
        user_tagged = [ tag for tag in p.split() if tag.startswith("@") ]
        imgs = request.FILES.getlist('files')
        print len(imgs)
        print wall_user
        if wall_user:
          s = Student.objects.get(user__username=wall_user)
        else:
          s = Student.objects.get(user= request.user)
        print s
        student = Student.objects.get(user=request.user)
        post = Post(text_content=p, post_date=timezone.now(), owner=student, wall_user=s)
        post.save()
        print post.wall_user
        if len(imgs)>0:
          for key in imgs:
            PI = PostImage(image = key,post = post)
            PI.save()
        for hash in hashed:
          print hash
          post.tags.add(hash)
        for user in user_tagged:
          user = user[1:]
          student_related = Student.objects.get(user__name=user)
          post.user_tags.add(student_related)
        data = {'temp':1}
# return  HttpResponse("post added")
        return HttpResponseRedirect(simplejson.dumps(data),'application/json')
      else:
        return HttpResponse('Hello')


@CORS_allow
def person_search(request):
   if request: #.is_ajax():
     q = request.GET.get('term','')
     print q
# import ipdb;ipdb.set_trace()
     students = Student.objects.filter(Q(user__name__icontains = q)).order_by('-user__name')[:10]
     def person_dict(student):
       return {
         'id':student.user.username,
         'label':str(student.user.name),
         'value':student.user.name
        }
     data = simplejson.dumps(map(person_dict,students))
   else:
     data = 'fail'
   return HttpResponse(data,'application/json')

#@csrf_exempt
#@CORS_allow
class TagIndexView(ListView):
      template_name = 'yaadein/tagged.html'
      model = Post
      context_object_name = 'posts_data'

      def get_queryset(self):
        posts_data = []
        posts = Post.objects.filter(tags__slug=self.kwargs.get('slug'))
        for post in posts:
          tmp = {
            'post': post,
            'images': PostImage.objects.filter(post=post)
          }
          posts_data.append( tmp )
        print "i"
        data = simplejson.dumps(posts_data)
        return HttpResponse(data, 'application/json')

"""
class tag_user(ListView):
     template_name='yaadein/usertag.html'
     model = Post
     context_object_name = 'posts'

     def get_queryset(self):
       s = Student.objects.get(user__username=self.kwargs.get('enrno'))
       return s.post_wall_user.all()
"""
