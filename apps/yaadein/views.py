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
import json as simplejson

@login_required
def index(request,enrno=None):
  y_user = YaadeinUser.objects.get_or_create(user=request.user)[0]
  s = Student.objects.get(user__username=enrno)
  posts = s.post_wall_user.all()
  posts_data = []
  for post in posts:
      tmp = {
             'post': post,
             'images': PostImage.objects.filter(post=post)
             }
      posts_data.append( tmp )

  return render_to_response('yaadein/usertag.html', {'cover_pic': y_user.coverpic.url,'enrno':enrno,'posts_data':posts_data}, context_instance=RequestContext(request))

@login_required
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
  #return render_to_response('yaadein/base.html',{},context_instance=requestContext(request))

def post(request,wall_user):
  if request.method == 'POST':
# import ipdb;ipdb.set_trace()
      print 'vaibhavraj'
      p = request.POST.get('content')
      hashed = [ word for word in p.split() if word.startswith("#") ]
      user_tagged = [ tag for tag in p.split() if tag.startswith("@") ]
      imgs = request.FILES.getlist('pic')
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
# return  HttpResponse("post added")
  return HttpResponseRedirect('/yaadein/'+ request.user.username)



def person_search(request):
   if request: #.is_ajax():
     q = request.GET.get('term','')
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
        return posts_data

"""
class tag_user(ListView):
     template_name='yaadein/usertag.html'
     model = Post
     context_object_name = 'posts'

     def get_queryset(self):
       s = Student.objects.get(user__username=self.kwargs.get('enrno'))
       return s.post_wall_user.all()
"""
