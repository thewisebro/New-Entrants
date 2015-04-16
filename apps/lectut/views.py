""" LECTUT VIEWS """

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.utils.encoding import smart_str
from django.contrib import messages
from django.conf import settings
from haystack.query import SearchQuerySet

from django.contrib.sessions.models import Session
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import mimetypes, os
import json

from nucleus.models import Batch, Course, User, Student , Faculty , RegisteredCourse
from forms import *
from models import *
from django import forms

DEVELOPMENT = settings.DEVELOPMENT
MEDIA_URL = settings.MEDIA_URL
GLOBAL_MEDIA_ROOT = settings.GLOBAL_MEDIA_ROOT

''' Decorator to handle cross origin requests '''
def CORS_allow(view):
  def wrapped_view(request, *args, **kwargs):
    if DEVELOPMENT:
      if request.method == 'POST':
        try:
          session_id = request.COOKIES['CHANNELI_SESSID']
          session = Session.objects.get(session_key=session_id)
          uid = session.get_decoded().get('_auth_user_id')
          user = User.objects.get(pk=uid)
          request.user = user
        except:
          pass

    response = view(request, *args, **kwargs)
    if DEVELOPMENT:
      response["Access-Control-Allow-Origin"] = "http://172.25.55.156:9008"
      response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
      response["Access-Control-Allow-Credentials"] = 'true'
#      response["Access-Control-Max-Age"] = "1000"
      response["Access-Control-Allow-Headers"] = "*"

    return response
  return wrapped_view

MAX_IMAGE_SIZE =  10485760     # 10 MB
MAX_PDF_SIZE = 20971520        # 20 MB
MAX_VIDEO_SIZE = 20971520      # 20 MB


# VIEWS

def get_post_dict(post):
  documents =  Uploadedfile.file_objects.all().filter(post=post)
  post = post.as_dict()
  files = []
  for document in documents:
    document = document.as_dict()
    files.append(document)
  return {'post':post,'files':files}


@csrf_exempt
@CORS_allow
def dispbatch(request):
  posts = []
  if request.user.is_authenticated():
    userType = getUserType(request.user)
    batches_info = []
    user_info = request.user.serialize()
    if userType == "0":
      student = request.user.student
      batches = student.batch_set.all()
      courses = map(lambda x: x.course, batches)
      batches_info = map(lambda x: batch_dict(x),batches)
      userPosts = Post.post_objects.all().order_by('-datetime_created')
#      index = settings.PROJECT_ROOT + '/apps/lectut/static/lectut-front/dist/index.html'
#      with open(index,'r') as f:
#       response =  HttpResponse(f.read())
#       return response
#return render(request, 'dist/index.html', context)
    elif userType == "1":
      faculty = request.user.faculty
      batches = faculty.batch_set.all()
      courses = map(lambda x: x.course, batches)
      batches_info = map(lambda x: batch_dict(x),batches)
      userPosts = Post.post_objects.all().order_by('-datetime_created')

    else:
      userPosts = Post.post_objects.all().filter(privacy = False).order_by('-datetime_created')
      user_info = 'Unknown'
    for post in userPosts:
      posts.append(get_post_dict(post))
    data = {'user': user_info,
            'batches': batches_info,
            'posts':posts,
            'userType': userType}

    return HttpResponse (json.dumps(data),content_type='application/json')

  latest_posts = Post.post_objects.all().filter(privacy = False).order_by('-datetime_created') #[number:(number+post_count)]
  for post in latest_posts:
    complete_post = get_post_dict(post)
    posts.append(complete_post)
  return HttpResponse (json.dumps({'posts':posts,'userType':"2"}),content_type='application/json')

@csrf_exempt
@CORS_allow
def latest_feeds(request):
  userType = getUserType(request.user)
  latest_posts = Post.post_objects.all().filter(privacy = True).order_by('-datetime_created')
  posts = []
  for post in latest_posts:
    posts.append(get_post_dict(post))
  return HttpResponse (json.dumps({'posts':posts, 'userType':userType}),content_type='application/json')

@csrf_exempt
@CORS_allow
#@login_required
def coursepage(request, batch_id):
    user = request.user
#    usrname = request.POST.get('user','harshithere')
#    user = User.objects.get(username=usrname)
    if not Batch.objects.filter(id=batch_id).exists():
      return HttpResponse(json.dumps('This batch doesnot exist'),content_type='application/json')
    userBatch = Batch.objects.get(id=batch_id)
    posts = []
    request.session['batchId'] = batch_id

    post_count = 10                      # Number of posts that are send in one attempt
    number = 0
    userType=getUserType(user)

    if userType == "0":
      if user.student in userBatch.students.all():
        previous_posts = Post.post_objects.all().filter(batch_id = batch_id).order_by('-datetime_created') #[number:(number+post_count)]
        in_batch = True
      else:
        previous_posts = Post.post_objects.all().filter(batch_id = batch_id).filter(privacy = False).order_by('-datetime_created')
        in_batch = False
    elif userType == "1":
      if user.faculty in userBatch.faculties.all():
        previous_posts = Post.post_objects.all().filter(batch_id = batch_id).order_by('-datetime_created') #[number:(number+post_count)]
        in_batch = True
      else:
        previous_posts = Post.post_objects.all().filter(batch_id = batch_id).filter(privacy = False).order_by('-datetime_created')
        in_batch = False
    else:
      previous_posts = Post.post_objects.all().filter(batch_id = batch_id).filter(privacy = False).order_by('-datetime_created')
      in_batch = False

    for post in previous_posts:
      complete_post = get_post_dict(post)
      posts.append(complete_post)

    context = {'posts': posts,
               'batch':batch_dict(userBatch),
               'userType':userType,
               'in_batch':in_batch,}

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

      if file_type!='Video' and  upload_file._size>MAX_IMAGE_SIZE:
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
    status = 100
    user = request.user
#    usrname = allData['user']
#    user = User.objects.get(username=usrname)
    if Batch.objects.filter(id = batch_id).exists():
      userBatch = Batch.objects.get(id = batch_id)
      course = userBatch.course
    elif Course.objects.filter(id = batch_id).exists():
      course = Course.objects.get(id = batch_id)
      userBatch = None
    else:
      return HttpResponse(json.dumps({'msg':'Invalid Course. Please contact IMG if problem persists' , 'status':102}), content_type='application/json')

#    data = request.POST.get('formText','')
    data = allData['formText']
    privacy = False
    uploadTypes = allData['typeData']
    documents = request.FILES.getlist('file')
    extra = request.POST.getlist('extra','')
    if not data and not documents:
      return HttpResponse(json.dumps({'msg':'Empty posts are not allowed','status':101}), content_type='application/json')
    if getUserType(user) == "1":
      privacy = allData['privacy']
    files = []
    msg = ''
    counter = 0
    try:
      if userBatch is not None:
        new_post = Post(upload_user = user, batch = userBatch, course = course, content = data , privacy = privacy)
      else:
        new_post = Post(upload_user = user, course = course, content = data , privacy = privacy)
      new_post.save()
    except:
      return HttpResponse(json.dumps({'msg':'Cannot save post','status':102}), content_type='application/json')
    for document in documents:
      file_type = getFileType(document)
#      fileData = json.loads(extra[counter])
      if file_type =='Video' and  document._size>MAX_VIDEO_SIZE:
        msg = "Video too large.Must be smaller than 20MB"
      if file_type =='pdf' and  document._size>MAX_PDF_SIZE:
        msg = "Image too large.Must be smaller than 20MB"
      elif document._size>MAX_IMAGE_SIZE:
        msg = "File too large.Must be smaller than 20MB"
      else:
        new_document = Uploadedfile(post =new_post, upload_file = document, description = str(document), file_type=file_type, upload_type = uploadTypes[counter])
        new_document.save()
        files.append(new_document.as_dict())
      counter = counter+1
    new_post.save()
    if msg !='':
#      response =  HttpResponse(json.dumps(msg), content_type='application/json')
      status = 101
    new_post = new_post.as_dict()
    complete_post = {'post':new_post,'files':files}
    response =  HttpResponse(json.dumps({'complete_post':complete_post,'status':status , 'msg':msg}), content_type='application/json')
  else:
    response = HttpResponse('It is not a post request')
  return response


def getFileType(file_name):
#mime = magic.Magic(mime=True)
#file_type = mime.from_file(file_name)
  file_name = str(file_name)
  try:
    extension = file_name.split(".")[-1]
    extension = extension.lower()
    if extension in ['jpg','png','jpeg','gif','exif','tiff']:
      file_type="image"
    elif extension=='pdf':
      file_type="pdf"
    elif extension in ['ppt', 'pptx' , 'pot','pptm','potx','potm','ppsx']:
      file_type="ppt"
    elif extension in ['dv', 'mov', 'mp4', 'avi', 'wmv', 'mkv', 'webm']:
      file_type="video"
    elif extension in ['gz','tar','iso','lbr','zip']:
      file_type="zip"
    elif extension in ['xlsx','xlsv','xls','ods']:
      file_type="sheet"
    else:
      file_type="other"
  except:
    file_type="other"
  return file_type


@csrf_exempt
@CORS_allow
def download_file(request, file_id):
  download_file = Uploadedfile.objects.get(id = file_id)
  path_to_file = os.path.join(MEDIA_URL, str(download_file.upload_file))
  download_file_open = download_file.upload_file.path
  file_check = open(download_file_open,"r")
#mimetype = mimetypes.guess_type(filename)[0]

#  user = User.objects.get(username = 'harshithere')
  downloadlog = DownloadLog(uploadedfile=download_file , user = request.user)
  downloadlog.save()
#  file_name = smart_str(download_file)

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
  try:
    if user.in_group('student'):
      return "0"
    elif user.in_group('faculty'):
      return "1"
    else:
      return "2"
  except:
    return "2"

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


@csrf_exempt  
@CORS_allow
def batch_data(request , batch_id):
  batch = Batch.objects.get(id = batch_id)
  batch_info = batch_dict(batch)
  response = HttpResponse(json.dumps(batch_info), content_type='application/json')
  return response

''' Show a particular post '''
@csrf_exempt
@CORS_allow
def get_post(request , batch_id , post_id):
  user = request.user
  if Post.objects.filter(id = post_id).exists():
    if Post.post_objects.filter(id = post_id).exists():
      post = Post.post_objects.get(id = post_id)
      complete_post = get_post_dict(post)
      if user.is_authenticated():
        return HttpResponse(json.dumps({'post':complete_post,'user_info':user.serialize() , 'status':100}), content_type='application/json')
      else:
        return HttpResponse(json.dumps({'post':complete_post , 'user_info':'' , 'status':100}), content_type='application/json')
    else:
      msg = 'Post has been deleted'
  else:
    msg = 'Post doesnot exist'

  response = HttpResponse(json.dumps({'msg':msg , 'status':101}), content_type='application/json')
  return response


@csrf_exempt
@CORS_allow
def get_file(request , batch_id , file_id):
  user = request.user
  if Uploadedfile.objects.filter(id = file_id).exists():
    if Uploadedfile.file_objects.filter(id = file_id).exists():
      File = Uploadedfile.file_objects.get(id = file_id)
      user = File.post.upload_user
      user_info = user.serialize()
      File = File.as_dict()
      if user.is_authenticated():
        return HttpResponse(json.dumps({'file':File , 'user_info':user_info , 'status':100}), content_type='application/json')
      else:
        return HttpResponse(json.dumps({'file':File , 'user_info':'' , 'status':100}), content_type='application/json')
    else:
      msg = 'File has been deleted'
  else:
    msg = 'File doesnot exist'

  response = HttpResponse(json.dumps({'msg':msg , 'status':101}), content_type='application/json')
  return response


@csrf_exempt
@CORS_allow
#@login_required
def deleteFile(request , file_id):
  user = request.user
  status = 101
  if Uploadedfile.file_objects.filter(pk=file_id).exists():
    fileToDelete = Uploadedfile.objects.get(pk=file_id)
    post = fileToDelete.post

    if user.in_group('faculty') or user == fileToDelete.post.upload_user:
      try:
        fileToDelete.delete()
        msg = 'File has been deleted'
        status = 100
        counter = Uploadedfile.file_objects.all().filter(post = post).count()
        if counter ==0 and post.content =='':
          post.delete()
          msg = 'The post has been deleted as well'
      except:
        msg = 'Some error Occured'
        status = 102
    else:
      msg = 'You are not authorised to delete this file. This shall be reported'
  else:
    msg='File doesnot exist'
  response = HttpResponse(json.dumps({'msg':msg,'status':status}), content_type='application/json')
  return response
#  return HttpResponseRedirect(reverse('coursepage' , kwargs={"batch_id":batch_id}))


@csrf_exempt
@CORS_allow
def deletePost(request , post_id):
  user = request.user
  status = 101
  if Post.post_objects.filter(pk=post_id).exists():
    postToDelete = Post.objects.get(pk=post_id)
    if user.in_group('faculty') or user == postToDelete.upload_user:
      try:
        postToDelete.delete()
        files = Uploadedfile.file_objects.all().filter(post=postToDelete)
        for afile in files:
          afile.delete()
        msg = 'Post has been deleted'
        status = 100
      except:
        msg = 'Kuch katta ho gaya'
        status = 102
    else:
      msg = 'You are not authorised to delete this post. This shall be reported'
  else:
    msg='Post doesnot exist'
  response = HttpResponse(json.dumps({'msg':msg , 'status':status}), content_type='application/json')
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
  if not Batch.objects.filter(id = batch_id).exists():
    return HttpResponse(json.dumps({'msg':'Batch Doesnot exist' , 'status':101}), content_type="application/json")
  currentBatch = Batch.objects.get(id = batch_id)
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

  members = {'students':students, 'faculties':faculties , 'status':100}

  return HttpResponse(json.dumps(members), content_type="application/json")


''' Gives all the files in a particular batch '''
@csrf_exempt
@CORS_allow
def get_files(request, batch_id):
  if not Batch.objects.filter(id = batch_id).exists():
    return HttpResponse(json.dumps({'msg':'Batch Doesnot exist' , 'status':101}), content_type="application/json")
  currentBatch = Batch.objects.get(id = batch_id)
  AllFiles = {'lec':[],'tut':[],'exp':[],'sol':[],'que':[]}
  currentFiles = Uploadedfile.file_objects.all().filter(post__batch_id = batch_id)
  for File in currentFiles:
    AllFiles[File.upload_type].append(File.as_dict())

  AllFiles['Lecture'] = AllFiles.pop('lec')
  AllFiles['Tutorial'] = AllFiles.pop('tut')
  AllFiles['Exam Papers'] = AllFiles.pop('exp')
  AllFiles['Solution'] = AllFiles.pop('sol')
  AllFiles['Question'] = AllFiles.pop('que')

  AllArchives = {'lec':[],'tut':[],'exp':[],'sol':[],'que':[]}
  currentCourse = currentBatch.course
  oldFiles =Uploadedfile.file_objects.all().filter(post__course_id = currentCourse.id).filter(post__batch_id__isnull = True)
  for File in oldFiles:
   AllArchives[File.upload_type].append(File.as_dict())

  AllArchives['Lecture'] = AllArchives.pop('lec')
  AllArchives['Tutorial'] = AllArchives.pop('tut')
  AllArchives['Exam Papers'] = AllArchives.pop('exp')
  AllArchives['Solution'] = AllArchives.pop('sol')
  AllArchives['Question'] = AllArchives.pop('que')

  files = {'currentFiles':AllFiles , 'archiveFiles':AllArchives , 'status':100}
  return HttpResponse(json.dumps(files), content_type="application/json")

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
#  import pdb;pdb.set_trace()
  if filter_model == None:
    query_post = SearchQuerySet().all().autocomplete(content_auto = value).models(Post)
    query_uploadfile = SearchQuerySet().all().autocomplete(description_auto = value).models(Uploadedfile)
    query_courses_name =  SearchQuerySet().all().autocomplete(name_auto = value).models(Course)
    query_courses_code =  SearchQuerySet().all().autocomplete(code_auto = value).models(Course)
  else:
    query = SearchQuerySet().autocomplete(content_auto = value).models(filter_model)

  final_posts , final_files ,posts , upload_files , batches , final_batches = [],[],[],[],[],[]
  try:
    posts = map(lambda result:Post.objects.get(id = result.pk) if Post.objects.filter(id=result.pk).exists() else None,query_post)
    upload_files = map(lambda result:Uploadedfile.objects.get(id = result.pk) if Uploadedfile.objects.filter(id=result.pk).exists() else None,query_uploadfile)
    courses = map(lambda result:Course.objects.get(id = result.pk),query_courses_name+query_courses_code)
    for course in courses:
      batches.append(Batch.objects.filter(course = course).all())
  except:
    pass

  final_posts = map(lambda result:result.as_dict() if (result is not None and result.deleted == False) else None,posts)
  final_files = map(lambda result:result.as_dict() if (result is not None and result.deleted == False) else None,upload_files)
  final_batches = map(lambda result:result.batch_dict() ,batches)

  results = {'posts':final_posts , 'files':final_files , 'courses':final_batches ,'status':100}
  return HttpResponse(json.dumps(results), content_type="application/json")


# VIEWS FOR INITIAL REGISTRATION

def create_batch(request):
  user = request.user
  data = json.loads(request.POST['data'])
  course = Course.objects.get(id = data['id'])
  userType = getUserType(user)
  if userType == "0":
    faculties = data['faculty']
    if not faculties:
      return HttpResponse(json.dumps('There must be atleast one faculty'), content_type='appliaction/json')
    try:
      batchToAdd = Batch(name = data['name'] , course= course)
      batchToAdd.save()
      for faculty in faculties:
        batch.faculties.add(faculty)
      batch.students.add(user)
    except:
      return HttpResponse(json.dumps('Insufficient data provided'), content_type='appliaction/json')
  elif userType == "1":
    try:
      batchToAdd = Batch(name = data['name'] , course= course)
      batchToAdd.save()
      batch.faculties.add(user)
    except:
      return HttpResponse(json.dumps('Insufficient data provided'), content_type='appliaction/json')
  else:
    return HttpResponse(json.dumps('This user cannot create a batch'), content_type='appliaction/json')

  return HttpResponse(json.dumps(batch.batch_dict()), content_type='appliaction/json')


def join_batch(request , batch_id):
  batch = Batch.objects.get(id = batch_id)
  user = request.user
  userType = getUserType(user)
  if userType == "0":
    batch.students.add(user)
  elif userType == "1":
    batch.faculties.add(user)
  else:
    return HttpResponse(json.dumps('This user cannot join this batch'), content_type='application/json')

  return HttpResponse(json.dumps(batch.batch_dict()), content_type='application/json')

def ini_batch_student(request):
  user = request.user
  student = user.student
  regis_courses = RegisteredCourse.objects.all().filter(student = student).filter(cleared_status = 'current')
  courses = []
  for regis_course in regis_courses:
    course = regis_course.course
    some_dict = {
                 'id':course.id,
                 'code':course.code,
                 'name':course.name,
    }
    courses.append(some_dict)

  batches = student.batch_set.all()
  batches_info = map(lambda x: batch_dict(x),batches)
  faculty_objects = Faculty.objects.all()
  faculties = []
  for faculty in faculty_objects:
    user = faculty.user
    some_dict = {
                 'department' : faculty.department,
                 'user_id': user.id,
                 'name':user.name,
    }
    faculties.append(some_dict)

  details = {'courses':courses , 'batches':batches_info , 'faculties':faculties}
  return HttpResponse(json.dumps(details) , content_type = 'application/json')

def ini_batch_faculty(request):
  user = request.user
  faculty = user.faculty
  return
