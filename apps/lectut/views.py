from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from nucleus.models import Batch, Course, User, Student
from forms import *
from models import *

# Create your views here.
'''def create_profile(request):
      try:
         upload_image  = Upload_Image.objects.get(user=request.user)
      except:
          pass
if request.method == 'POST':
      form = CreateProfileForm(request.POST, request.FILES)

else:
    form = CreateProfileForm(request.POST or None, instance=upload_image)
    return render_to_response('profile.html', locals(), context_instance=RequestContext(request))
'''
def tester(request):
      return HttpResponse("Hello, world. You're at lectut.")

def dispbatch(request):
  active = request.user.is_active
  if active:
      student = request.user.student
      batches = student.batch_set.all()
      courses = map(lambda x: x.course, batches)
      context = {'courses': courses}
      return render(request, 'lectut/courses.html', context)
  else:
      return HttpResponse("Please log-in to view your courses")

def coursepage(request, course_name):
      return HttpResponse("bla bla")

def upload(request):
#context={'image_form' : image_form}
#return render (request, 'lectut/image.html', context)
   if request.method == 'POST':
           text_form = TextUpload(request.POST)
           image_form = ImageForm(request.POST , request.FILES )
           if text_form.is_valid():
              text_form.save()
              return HttpResponseRedirect(reverse('upload'))

           elif image_form.is_valid():
              new_image = UploadImage(upload_image = request.FILES['upload_image'])
              new_image.save()
              a1=Activity(log=new_image)
              a1.save()
              return HttpResponseRedirect(reverse('upload'))
   else:
      text_form = TextUpload()
      image_form = ImageForm()

   previous_noti=UploadImage.objects.all().order_by('-datetime_created')

   context = {'image_form': image_form,
              'text_form' : text_form,
              'previous_noti': previous_noti}
   return render( request, 'lectut/image.html', context)
