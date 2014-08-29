from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from django.core.exceptions import ValidationError
from django.contrib import messages
from settings import *

#import mimetypes, magic
import mimetypes, os
import json as simplejson

from nucleus.models import Batch, Course, User, Student
from forms import *
from models import *
from django import forms

# Create your views here.
def tester(request):
      return HttpResponse("Hello, world. You're at lectut.")

MAX_FILE_SIZE =  524   #5242880
MAX_VIDEO_SIZE = 20971520

def dispbatch(request):
  active = request.user.is_active
  if active:
    if request.user.in_group('student'):
      student = request.user.student
      batches = student.batch_set.all()
      courses = map(lambda x: x.course, batches)
      context = {'courses': courses,
                 'batches': batches}
      return render(request, 'lectut/courses.html', context)
    elif request.user.in_group('faculty'):
      return HttpResponse("You are a faculty")
  else:
      return HttpResponse("Please log-in to view your courses")

@login_required
def coursepage(request, batch_id):
  user = request.user
  userBatch = Batch.objects.get(id=batch_id)
  request.session['batchId'] = batch_id
  userType=getUserType(user)
  text_form = TextForm()
  image_form = FileForm()

  previous_uploads=UploadFile.objects.all().filter(batch_id=batch_id).order_by('-datetime_created')

  context = {'image_form': image_form,
             'text_form' : text_form,
             'previous_uploads': previous_uploads,
             'batch':userBatch,
             'userType':userType,
             'viewType':'Coursepage'}
  return render( request, 'lectut/image.html', context)

def uploadFile(request , batch_id):
  user = request.user
  userBatch = Batch.objects.get(id=batch_id)
  if request.method == 'POST':
    text_form = TextForm(request.POST)
    file_form = FileForm(request.POST , request.FILES )
    if text_form.is_valid():
      new_notice=TextNotice(text=request.POST['text'] , upload_user=user,batch=userBatch)
      new_notice.save()
      notice_activity = Activity(Upload=new_notice)
      notice_activity.save()
      return HttpResponse(simplejson.dumps(new_notice), content_type="application/json")
#      return HttpResponseRedirect(reverse('coursepage' , kwargs={"batch_id":batch_id}))

    elif file_form.is_valid():
      upload_file = request.FILES['filename']
      file_type = getFileType(upload_file)
      upload_type = request.POST['upload_type']
      file_name=request.POST['upload_name']

#if file_type!='Video' and  upload_file._size>MAX_FILE_SIZE:
#file_form.errors['__all__']=file_form.error_class(["File too large.Must be smaller than 5MB"])
#       msg = "File too large"
# return HttpResponse(simplejson.dumps(msg, mime_type='application/json')
#elif upload_file._size>MAX_VIDEO_SIZE:
#        raise file_form.ValidationError("Video too large.Must be smaller than 20MB")

      new_file = UploadFile(upload_file = upload_file, file_type=file_type, upload_user=user, name=file_name ,batch=userBatch , upload_type=upload_type , privacy=False)
      new_file.save()
      file_activity = Activity(Upload=new_file)
      file_activity.save()
      return HttpResponse(simplejson.dumps(new_file), content_type="application/json")
#      return HttpResponseRedirect(reverse('coursepage' , kwargs={"batch_id":batch_id}))

def getFileType(file_name):
#mime = magic.Magic(mime=True)
#file_type = mime.from_file(file_name)
  extension = file_name.name.split(".")[1]
  if extension in ['jpg','png','jpeg','gif']:
    file_type="image"
  elif extension=='pdf':
    file_type="pdf"
  elif extension=='ppt':
    file_type="ppt"
  elif extension in ['dv', 'mov', 'mp4', 'avi', 'wmv']:
    file_type="video"
  else:
    file_type="unknown"
  return file_type

def download_file(request, file_id):
  download_file = UploadFile.objects.get(id = file_id)
  path_to_file = os.path.join(MEDIA_URL, str(download_file.upload_file))
  download_file_open = download_file.upload_file.path
  file = open(download_file_open,"r")
#mimetype = mimetypes.guess_type(filename)[0]

  downloadlog = DownloadLog(uploadfile=download_file , user = request.user)
  downloadlog.save()

  response = HttpResponse(mimetype='application/force-download')
#response = HttpResponse(file.read(), mimetype=mimetype)
  response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(download_file)
  response['X-Sendfile'] = smart_str(download_file_open)
  return response

def get_path_to_file(file_name):
  return MEDIA_URL/file_name.upload_file

def getUserType(user):
  if user.in_group('faculty'):
    return "1"
  else:
    return "0"

@login_required
def delete(request , file_id):
  user = request.user
  batch_id = request.session['batchId']
  if request.user.in_group('faculty'):
    UploadFile.objects.get(pk=file_id).delete()
  return HttpResponseRedirect(reverse('coursepage' , kwargs={"batch_id":batch_id}))

def useruploads(request , batch_id):
  user = request.user
  userType=getUserType(user)
  userBatch = Batch.objects.get(id=batch_id)
  if batch_id == 'all':
    required_files = UploadFile.objects.all().filter(upload_user=user).order_by('-datetime_created')
  else:
    required_files = UploadFile.objects.all().filter(upload_user=user).filter(batch_id=batch_id).order_by('-datetime_created')

  content= {#'previous_uploads':required_files,
#'userBatch':userBatch,
            'userType':userType,
            'viewType':'MyUploads'}
#return render(request,'lectut/image.html',context)
  return HttpResponse(simplejson.dumps(content), content_type="application/json")

def userdownloads(request , batch_id):
  user = request.user
  userType=getUserType(user)
  userBatch = Batch.objects.get(id=batch_id)
  fileIds = DownloadLog.objects.all().filter(user=user)
  if batch_id=='all':
    required_files=UploadFile.objects.all().filter(id__in=fileIds).order_by('-datetime_created')
  else:
    required_files=UploadFile.objects.all().filter(id__in=fileIds).filter(batch_id=batch_id).order_by('-datetime_created')
  context= {'previous_uploads':required_files,
            'userBatch':userBatch,
            'userType':userType,
            'viewType':'MyDownloads'}
#return render(request,'lectut/image.html',context)
  return HttpResponse(simplejson.dumps(context), content_type="application/json")

#def upload(request):
#   user = request.user
#   userBatch = Batch.objects.get(id=1)
##context={'image_form' : image_form}
##return render (request, 'lectut/image.html', context)
#   if request.method == 'POST':
#           text_form = TextUpload(request.POST)
#           image_form = ImageForm(request.POST , request.FILES )
#           if text_form.is_valid():
#             new_notice=TextNotice(text=request.POST['text'] , upload_user=user,batch=userBatch)
#             new_notice.save()
#             return HttpResponseRedirect(reverse('upload'))
#
#           elif image_form.is_valid():
#              new_image = UploadImage(upload_image = request.FILES['upload_image'])
#              new_image.save()
##a1=Activity(log=new_image)
##             a1.save()
#              return HttpResponseRedirect(reverse('upload'))
#   else:
#      text_form = TextUpload()
#      image_form = ImageForm()
#
#   previous_noti=UploadImage.objects.all().order_by('-datetime_created')
#
#   context = {'image_form': image_form,
#              'text_form' : text_form,
#              'previous_noti': previous_noti}
#   return render( request, 'lectut/image.html', context)
