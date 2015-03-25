""" LECTUT VIEWS """

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from django.utils.encoding import smart_str
from django.contrib import messages
from django.conf import settings
from haystack.query import SearchQuerySet

from django.contrib.sessions.models import Session
from settings.development import PRODUCTION, MEDIA_URL , GLOBAL_MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt

import mimetypes, os
import json

from nucleus.models import Batch, Course, User, Student
from forms import *
from models import *
from django import forms


''' Decorator to handle cross origin requests '''
def CORS_allow(view):
  def wrapped_view(request, *args, **kwargs):
    if PRODUCTION == False:
      if request.method == 'POST':
        session_id = request.COOKIES['CHANNELI_SESSID']
        session = Session.objects.get(session_key=session_id)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        request.user = user

    response = view(request, *args, **kwargs)
    if PRODUCTION == False:
      response["Access-Control-Allow-Origin"] = "http://172.25.55.156:9008"
      response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
      response["Access-Control-Allow-Credentials"] = 'true'
#      response["Access-Control-Max-Age"] = "1000"
      response["Access-Control-Allow-Headers"] = "*"

    return response
  return wrapped_view

MAX_FILE_SIZE =  5242880       # 5 MB
MAX_VIDEO_SIZE = 20971520      # 20 MB


# VIEWS
@CORS_allow
def dispbatch(request):
  active = request.user.is_authenticated
  if active:
    userType = getUserType()
    if request.user.in_group('Student'):
      student = request.user.student
      batches = student.batch_set.all()
      courses = map(lambda x: x.course, batches)
      context = {'courses': courses,
                 'batches': batches}
#      index = settings.PROJECT_ROOT + '/apps/lectut/static/lectut-front/dist/index.html'
#      with open(index,'r') as f:
#       response =  HttpResponse(f.read())
#       return response
#return render(request, 'dist/index.html', context)
    elif request.user.in_group('Faculty'):
      return HttpResponse("You are a faculty")
#    else:
#      return HttpResponse("You are not enrolled.Please visit IMG")
  else:
      return HttpResponse("Please log-in to view your courses")


@csrf_exempt
@CORS_allow
#@login_required
def coursepage(request, batch_id):
    user = request.user
#    usrname = request.POST.get('user','harshithere')
#    user = User.objects.get(username=usrname)
    userBatch = Batch.objects.get(id=batch_id)
    posts = []
    request.session['batchId'] = batch_id

    post_count = 10                      # Number of posts that are send in one attempt
    number = 0
    userType=getUserType(user)

    previous_posts = Post.post_objects.all().filter(batch_id = batch_id).order_by('-datetime_created') #[number:(number+post_count)]
    for post in previous_posts:
      documents =  Uploadedfile.file_objects.all().filter(post=post)
      post = post.as_dict()
      files = []
      for document in documents:
        document = document.as_dict()
        files.append(document)
      complete_post = {'post':post,'files':files}
      posts.append(complete_post)

    context = {'posts': posts,
#               'batch':userBatch,
               'userType':userType,
               'viewType':'Coursepage'}

    return HttpResponse(json.dumps(context),content_type='application/json')
#    return render( request, 'lectut/image.html', context)


''' This was used when upload was done by forms. Became disfunct when upload was ajaxified '''
def uploadFile(request , batch_id):
  user = request.user
  userBatch = Batch.objects.get(id=batch_id)
#import pdb;pdb.set_trace();
  if request.method == 'POST':
    text_form = TextForm(request.POST)
    file_form = FileForm(request.POST , request.FILES )
    if text_form.is_valid():
      new_notice=TextNotice(text=request.POST['text'] , upload_user=user,batch=userBatch)
      new_notice.save()
      notice_activity = Activity(Upload=new_notice)
      notice_activity.save()
      new_notice=new_notice.as_dict()
      return HttpResponse(json.dumps(new_notice), content_type="application/json")

    elif file_form.is_valid():
      upload_file = request.FILES['filename']
      file_type = getFileType(upload_file)
      upload_type = request.POST['upload_type']
      file_name=request.POST['upload_name']
#import pdb;pdb.set_trace();

      if file_type!='Video' and  upload_file._size>MAX_FILE_SIZE:
        msg = "File too large.Must be smaller than 5MB"
      elif upload_file._size>MAX_VIDEO_SIZE:
        msg = "Video too large.Must be smaller than 20MB"
      else:
        new_file = UploadFile(upload_file = upload_file, file_type=file_type, upload_user=user, name=file_name ,batch=userBatch , upload_type=upload_type , privacy=False)
        new_file.save()
        file_activity = Activity(Upload=new_file)
        file_activity.save()
        return HttpResponse(json.dumps(new_file.as_dict()), content_type='application/json')
    else:
      msg = "Please fill all the fields"

    if msg:
      return HttpResponse(json.dumps(msg), content_type='application/json')
    else:
      return 0
#return HttpResponseRedirect(reverse('coursepage' , kwargs={"batch_id":batch_id}))

@csrf_exempt
@CORS_allow
def uploadedFile(request , batch_id):
  if request.method == 'POST':
    allData = json.loads(request.POST['data'])
    user = request.user
#    usrname = allData['user']
#    user = User.objects.get(username=usrname)
    userBatch = Batch.objects.get(id=batch_id)
#    data = request.POST.get('formText','')
    data = allData['formText']
    uploadTypes = allData['typeData']
    documents = request.FILES.getlist('file')
    extra = request.POST.getlist('extra','')
    files = []
    msg = ''
    counter = 0
    try:
      new_post = Post(upload_user = user, batch = userBatch, content = data)
      new_post.save()
    except:
      msg = "Cannot save post"
    for document in documents:
      file_type = getFileType(document)
#      fileData = json.loads(extra[counter])
      if file_type!='Video' and  document._size>MAX_FILE_SIZE:
        msg = "File too large.Must be smaller than 5MB"
      elif document._size>MAX_VIDEO_SIZE:
        msg = "Video too large.Must be smaller than 20MB"
      else:
        new_document = Uploadedfile(post =new_post, upload_file = document, description = str(document), file_type=file_type, upload_type = uploadTypes[counter])
        new_document.save()
        files.append(new_document.as_dict())
      counter = counter+1
    if msg !='':
      response =  HttpResponse(json.dumps(msg), content_type='application/json')
    else:
      new_post = new_post.as_dict()
      complete_post = {'post':new_post,'files':files}
      response =  HttpResponse(json.dumps(complete_post), content_type='application/json')
  else:
    response = HttpResponse('It is not a post request')
  return response


def getFileType(file_name):
#mime = magic.Magic(mime=True)
#file_type = mime.from_file(file_name)
  file_name = str(file_name)
  try:
    extension = file_name.split(".")[1]
    extension = extension.lower()
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
  except:
    file_type="unknown"
  return file_type


@csrf_exempt
@CORS_allow
def download_file(request, file_id):
  download_file = Uploadedfile.objects.get(id = file_id)
  path_to_file = os.path.join(MEDIA_URL, str(download_file.upload_file))
  download_file_open = download_file.upload_file.path
  file_check = open(download_file_open,"r")
#mimetype = mimetypes.guess_type(filename)[0]

  user = User.objects.get(username = 'harshithere')
#  downloadlog = DownloadLog(uploadfile=download_file , user = user)
#  downloadlog.save()

#  response = HttpResponse(file_check.read(),content_type='application/force-download')
  response = HttpResponse(file_check.read(),content_type='application/octet-stream')
#response = HttpResponse(file.read(), mimetype=mimetype)
  response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(download_file)
  response['X-Sendfile'] = smart_str(download_file_open)
  return response

def get_path_to_file(file_name):
  return MEDIA_URL/file_name.upload_file


''' Function to differentiate between faculty and students '''
def getUserType(user):
  if user.in_group('faculty'):
    return "1"
  else:
    return "0"

def batch_dict(Batch):
  batch_info = {
                'id':Batch.id,
                'credits':Batch.course.credits,
                'name': Batch.name,
                'course_name':Batch.course.name,
                'code':Batch.course.code,
                'subject_area':Batch.course.subject_area,
                'semtype':Batch.course.semtype,
                'year':Batch.course.year
               }
  return batch_info

''' Show a particular post '''
@csrf_exempt
@CORS_allow
def get_post(request , batch_id , post_id):
  user = request.user
  if Post.objects.get(id = post_id).exists():
    if Post.post_objects.get(id = post_id).exists():
      post = Post.post_objects.get(id = post_id)
      documents =  Uploadedfile.file_objects.all().filter(post=post)
      post = post.as_dict()
      files = []
      for document in documents:
        document = document.as_dict()
        files.append(document)
      complete_post = {'post':post,'files':files}
      return HttpResponse(json.dumps(complete_post), content_type='application/json')
    else:
      msg = 'Post has been deleted'
  else:
    msg = 'Post doesnot exist'

  response = HttpResponse(json.dumps(msg), content_type='application/json')
  return response


@csrf_exempt
@CORS_allow
#@login_required
def deleteFile(request , file_id):
  user = request.user
  if Uploadedfile.file_objects.filter(pk=file_id).exists():
    fileToDelete = Uploadedfile.objects.get(pk=file_id)

    if user.in_group('faculty') or user == fileToDelete.post.upload_user:
      try:
        fileToDelete.delete()
        msg = 'File has been deleted'
      except:
        msg = 'Some error Occured'
    else:
      msg = 'You are not authorised to delete this file. This shall be reported'
  else:
    msg='File doesnot exist'
  response = HttpResponse(json.dumps(msg), content_type='application/json')
  return response
#  return HttpResponseRedirect(reverse('coursepage' , kwargs={"batch_id":batch_id}))


@csrf_exempt
@CORS_allow
def deletePost(request , post_id):
  user = request.user
  if Post.post_objects.filter(pk=post_id).exists():
    postToDelete = Post.objects.get(pk=post_id)
    if user.in_group('faculty') or user == postToDelete.upload_user:
      try:
        postToDelete.delete()
        files = Uploadedfile.file_objects.all().filter(post=postToDelete)
        for afile in files:
          afile.delete()
        msg = 'Post has been deleted'
      except:
        msg = 'Kuch katta ho gaya'
    else:
      msg = 'You are not authorised to delete this post. This shall be reported'
  else:
    msg='Post doesnot exist'
  response = HttpResponse(json.dumps(msg), content_type='application/json')
  return response

# Not used currently
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
  return HttpResponse(json.dumps(content), content_type="application/json")


# Not used currently
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
  return HttpResponse(json.dumps(context), content_type="application/json")


''' Gives all the members of a Batch '''
@csrf_exempt
@CORS_allow
def batchMembers(request , batch_id):
  currentBatch = Batch.objects.get(id = batch_id)
  import pdb;pdb.set_trace()
  students = currentBatch.students.all()
  users = map(lambda x:x.user, students)
  students =[]
  for user in users:
    user = user.serialize()
    students.append(user)

  faculties = currentBatch.faculties.all()
  users =  map(lambda x:x.user, faculties)
  faculties = []
  for user in users:
    user = user.serialize()
    faculties.append(user)

  members = {'students':students, 'faculties':faculties}

  return HttpResponse(json.dumps(members), content_type="application/json")


''' Gives all the files in a particular batch '''
@csrf_exempt
@CORS_allow
def get_files(request, batch_id):
  currentBatch = Batch.objects.get(id = batch_id)
  AllFiles = {'lec':[],'tut':[],'exp':[],'sol':[],'que':[]}
  files = Uploadedfile.file_objects.all().filter(post__batch_id = batch_id)
  for File in files:
    AllFiles[File.upload_type].append(File.as_dict())

  return HttpResponse(json.dumps(AllFiles), content_type="application/json")

@csrf_exempt
@CORS_allow
def post_comments(request , post_id):
  post = Post.post_objects.get(id = post_id)
  return render(request,'comments/comments.html',{'instance': post})


''' Creates a event/reminder '''
@csrf_exempt
@CORS_allow
def createReminder(request):
  if request.method == 'POST':
    if ReminderForm.is_valid():
      user = request.user
      batch = request.Session['batch_id']
      text = request.POST['text']
      time = datetime.now()
      ReminderToAdd = Reminders(text = text , batch = batch , user = user, event_date = time)
      ReminderToAdd.save()
      msg = "Event has been added"
    else:
      msg = "Invalid entry"
    return HttpResponse(json.dumps(msg), content_type="application/json")


''' Gives all events/reminders that will expire after current time '''
@csrf_exempt
@CORS_allow
def getReminder(request):
  student = request.user.student
  batches = student.batch_set.all()
  reminders = Reminders.objects.all().filter(batch__in=batches).filter(datetime_created >=timezone.now()).order_by('event_date')

  # Adds dictionary of each reminder in events
  events=[]
  for reminder in reminders:
    events.append(reminder.as_dict())
  return HttpRsponse(json.dumps(events), content_type="application/json")


''' View for search using Haystack Elasticsearch '''
@csrf_exempt
@CORS_allow
def search(request):
  value = request.GET.get('q')
  filter_model = request.GET.get('model')
  if filter_model == None:
    query_post = SearchQuerySet().all().autocomplete(content_auto = value).models(Post)
    query_uploadfile = SearchQuerySet().all().autocomplete(filename_auto = value).models(Uploadedfile)
    query_courses =  SearchQuerySet().all().autocomplete(name_auto = value).models(Course)
  else:
    query = SearchQuerySet().autocomplete(content_auto = value).models(filter_model)

  final_posts = []
  final_files = []
  posts = map(lambda result:Post.objects.get(id = result.pk),query_post)
  upload_files = map(lambda result:Uploadedfile.objects.get(id = result.pk),query_uploadfile)
  courses = map(lambda result:{'name':result.name,'code':result.code},query_courses)

  final_posts = map(lambda result:result.as_dict(),posts)
  final_files = map(lambda result:result.as_dict(),upload_files)

  results = {'posts':final_posts , 'files':final_files , 'courses':courses }
  return HttpResponse(json.dumps(results), content_type="application/json")
