from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from yaadein.models import Post,PostImage
from django.shortcuts import get_object_or_404
from django.utils import timezone
from taggit.models import Tag,TaggedItem
from django.views.generic import DetailView, ListView
from nucleus.models import Student,User

@login_required
def index(request):
  if request.method == 'POST':
    p = request.POST.get('content')
    hashed = [ word for word in p.split() if word.startswith("#") ]
    user_tagged = [ tag for tag in p.split() if tag.startswith("@") ]
    img = request.FILES.get('pic')
    student = Student.objects.get(user=request.user)
    post = Post(text_content=p, post_date=timezone.now(), owner=student, wall_user=student)
    post.save()
    if img:
      PI = PostImage(image = img,post = post)
      PI.save()
    for hash in hashed:
      print hash
      post.tags.add(hash)
    for user in user_tagged:
      user = user[1:]
      student_related = Student.objects.get(user__name=user)
      post.user_tags.add(student_related)
    return  HttpResponse("post added")

  return render_to_response('yaadein/base.html',{},context_instance=RequestContext(request))


def person_search(request):
   if request.is_ajax():
     q = request.GET.get('term','')
     students = Student.objects.filter(Q(name__icontains = q)).order_by('-user__name')[:10]
     def person_dict(person):
       return {
         'id':Student.user.name,
         'label':str(Student.user.name),
         'value':Student.user.name
        }
     data = simplejson.dumps(map(person_dict,students))
   else:
     data = 'fail'
   return HttpResponse(data,'application/json')


class TagIndexView(ListView):
      template_name = 'yaadein/tagged.html'
      model = Post
      context_object_name = 'posts'

      def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('slug'))

class tag_user(ListView):
     template_name='yaadein/usertag.html'
     model = Post
     context_object_name = 'posts'

     def get_queryset(self):
       s = Student.objects.get(user__username=self.kwargs.get('enrno'))
       return s.post_wall_user.all()

