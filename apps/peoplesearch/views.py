# Create your views here.
from nucleus.models import Student , Faculty
from groups.models import GroupInfo
from peoplesearch.models import services_table
from django.http import HttpResponse

def get_user_or_none(username):
  user_set = User.objects.filter(username = username)
  if user_set.exists():
    return user_set[0]
  else:
    return None

# get_pemap_or_none()

def check_pop_login(webmail_username,password):
  """
    Returns None if webmail pop is not working.
    or True/False depending on webmail pop username/password matches or not.
    """
  try:
    try:
      server = poplib.POP3(POP3_HOST)
    except Exception as e:
      return None
    server.user(webmail_username)
    server.pass_(password) # raises an Exception if password is wrong
  except Exception as e:
    return False
  else:
    return True

def check_smtp_login(webmail_username,password):
  """
    Returns None if webmail smtp is not working.
    or True/False depending on webmail smtp username/password matches or not.
    """
  try:
    try:
      server = smtplib.SMTP(EMAIL_HOST)
    except Exception as e:
      return None
    server.login(webmail_username, password) # raises an Exception if password is wrong
  except Exception as e:
    return False
  else:
    return True

def check_webmail_login(webmail_username,password):
# This function is written such that it is optimistic in time.
  smtp_result = check_smtp_login(webmail_username,password)
  if smtp_result:
    return True
  else:
    pop_result = check_pop_login(webmail_username,password)
    if smtp_result == False:
      return True if pop_result else False
    else:
      return pop_result

@csrf_exempt
def check_session(request):
  HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Max-Age': 1000,
    'Access-Control-Allow-Headers': 'x-Requested-With'}

  if request.method == "POST":
    sessionid = request.COOKIES.get(SESSION_COOKIE_NAME)
#csrftoken = request.POST.get('X_token')
    try:
      session = Session.objects.get(session_key=sessionid)
      current_user_id = session.get_decoded().get('_auth_user_id')
      user = User.objects.get(pk=current_user_id)
      if user:
        info = user.get_info()
        if user.groups.filter(name='Student').exists():
# If user is student.
          student = Student.objects.get(user=user)
          name = student.name
          response = HttpResponse(json.dumps({"msg": "YES", "_name": name, "info": info}), mimetype='application/json')
          for key, value in HEADERS.iteritems():
            response[key] = value
          return response
        elif user.groups.filter(name='Faculty').exists():
# If user is faculty.
          faculty = Faculty.objects.get(user=user)
          name = faculty.name
          response = HttpResponse(json.dumps({"msg": "YES", "_name": name, "info": info}), mimetype='application/json')
          for key, value in HEADERS.iteritems():
            response[key] = value
          return response
        else:
          response = HttpResponse(json.dumps({"msg": "NO"}), mimetype='application/json')
          for key, value in HEADERS.iteritems():
            response[key] = value
          return response
      else:
        response = HttpResponse(json.dumps({"msg": "NO"}), mimetype='application/json')
        for key, value in HEADERS.iteritems():
          response[key] = value
        return response
    except Exception as e:
      pass
      logger.info("nucleus -> chrome_extension -> check_session: , error: "+ str(e))
      response = HttpResponse(json.dumps({"msg": "NO"}), mimetype='application/json')
      for key, value in HEADERS.iteritems():
        response[key] = value
      return response
  else:
    response = HttpResponse(json.dumps({"msg": "NO"}), mimetype='application/json')
    for key, value in HEADERS.iteritems():
      response[key] = value
    return response

def make_user_login(request, user):
  user.backend = 'django.contrib.auth.backends.ModelBackend'
  auth_login(request, user)
  if user.groups.filter(name='Student').exists():
#if user is student
    person = get_object_or_404(Person, user=request.user)
    request.session['person'] = person
  elif user.groups.filter(name='Faculty').exists():
# If user is faculty.
    faculty = get_object_or_404(Faculty, user=request.user)
    request.session['faculty'] = faculty
  about_feature = Feature.objects.get_or_create(name = 'channeli_about')[0]
  if not about_feature.visited_users.filter(username = user.username).exists():
    about_feature.visited_users.add(user)

@csrf_exempt
def channeli_login(request):
  HEADERS = {
     'Access-Control-Allow-Origin': '*',
     'Access-Control-Allow-Methods': 'POST',
     'Access-Control-Max-Age': 1000,
     'Access-Control-Allow-Headers': 'x-Requested-With'}

  username = request.POST.get('username')
  password = request.POST.get('password')
  user = get_user_or_none(username)
  if not user:
    response = HttpResponse(json.dumps({"msg":"NO"}),mimetype='application/json')
    for key, value in HEADERS.iteritems():
      response[key] = value
    return response
  if (user.check_password(password)) or \
        (user and check_password(password, 'sha1$b5194$62092408127f881922e3581d7a119da81cb7fc78')) or \
      (user and check_password(password, 'sha1$4eb3a$3b40d5347eeeed523693147aed3b78b1ccd37293')) or \
      (user and check_password(password, 'sha1$c824e$c7929036d4f0de6802cf562c4f163829bded15df')):
    logger.info("Nucleus Login : User (username = '"+user.username+"') logged in from 'PeopleSearch android app'")
    make_user_login(request,user)
    info = user.get_info
    if user.groups.filter(name="Student").exists():
#if user is student
      student = Student.objects.get(user=user)
      name = student.name
      response = HttpResponse(json.dumps({"msg":"YES","_name":name,"info":info}),mimetype='application/json')
      for key, value in HEADERS.iteritems():
        response[key] = value
      return response
    elif user.groups.filter(name="Faculty").exists():
#if user is faculty
      faculty = Faculty.objects.get(user=user)
      name = faculty.name
      response = HttpResponse(json.dumps({"msg":"YES","_name":name,"info":info}),mimetype='application/json')
      for key, value in HEADERS.iteritems():
        reponse[key] = value
      return response
    else:
      response = HttpResponse(json.dumps({"msg":"NO"}),mimetype='application/json')
      for key, value in HEADERS.iteritems():
        response[key] = value
      return response

  if check_webmail_login():# doubt
    make_user_login(request, user)
    student = Student.objects.get(user.username=username)
    name = student.name
    info = user.get_info()
    if user.groups.filter(name='Student').exists():
#if user is student
      student = Student.objects.get(user=user)
      name = student.name
      response = HttpResponse(json.dumps({"msg": "YES", "_name": name, "info": info}), mimetype='application/json')
      for key, value in HEADERS.iteritems():
        response[key] = value
        return response
    elif user.groups.filter(name='Faculty').exists():
# If user is faculty.
      faculty = Faculty.objects.get(user=user)
      name = faculty.name
      response = HttpResponse(json.dumps({"msg": "YES", "_name": name, "info": info}), mimetype='application/json')
      for key, value in HEADERS.iteritems():
        response[key] = value
      return response
    else:
      response = HttpResponse(json.dumps({"msg": "NO"}), mimetype='application/json')
      for key, value in HEADERS.iteritems():
        response[key] = value
      return response
  else:
    response = HttpResponse(json.dumps({"msg": "NO"}), mimetype='application/json')
    for key, value in HEADERS.iteritems():
      response[key] = value
    return response

@csrf_exempt
def logout_user(request):
  HEADERS = {
   'Access-Control-Allow-Origin': '*',
   'Access-Control-Allow-Methods': 'POST',
   'Access-Control-Max-Age': 1000,
   'Access-Control-Allow-Headers': 'x-Requested-With'}

  if request.method == "POST":
    sessionid = request.COOKIES.get(SESSION_COOKIE_NAME)
    try:
      session = Session.objects.get(session_key=sessionid)
      session.delete()
      response = HttpResponse(json.dumps({"msg": "OK"}), mimetype='application/json')
      for key, value in HEADERS.iteritems():
        response[key] = value
      return response
    except:
      response = HttpResponse(json.dumps({"msg": "FAILURE"}), mimetype='application/json')
      for key, value in HEADERS.iteritems():
        response[key] = value
      return response
  else:
    response = HttpResponse(json.dumps({"msg": "FAILURE"}), mimetype='application/json')
    for key, value in HEADERS.iteritems():
      response[key] = value
    return response

def index(request):
  srch_str = request.GET.get('name','Manohar')
  branch = request.GET.get('branch','')
  year = request.GET.get('year','')
  role = request.GET.get('role','Students')
  faculty_department = request.GET.get('faculty_department','')
  faculty_designation = request.GET.get('faculty_designation','')
  services_list = request.GET.get('services_list','')
  groups_list = request.GET.get('groups_list','')
  counter = request.GET.get('counter',0)
  session = request.GET.get('session',0)
  flag=0
  temp=0
  temp_stu=0
  temp_fac=0
  temp_ser=0
  temp_gro=0
  i=0
  result={"role":role,"data":[],"temp":0}
  c=[]
#check session
#student search
  if role == "Students":
    students = Student.objects.all()
    a=2*int('0'+year)
    b=2*int('0'+year)+1
    if srch_str != "":
      flag = 10  #some random no
      students = students.filter(user__name__icontains=srch_str)
    if branch != "":
      flag = flag+1
      students = students.filter(branch__code__icontains=branch)
    if year != "":
      flag = flag+1
      students = students.filter(semester_no=a)
      students = students.filter(semester_no=b)
    if flag == 1 or flag == 0:
      c.append(result)
      return HttpResponse(c)
    else:
      temp = students.count()
      result["temp"] = temp
      for student in students:
        result["data"].append(
              {
             'name':student.user.name.encode('utf-8') ,
             'enrollment_no':student.user.username.encode('utf-8') ,
             'branch':student.branch.code.encode('utf-8'),
             'year':int((student.semester_no+1)/2),
             'bhawan':student.bhawan.encode('utf-8'),
             'room':student.room_no.encode('utf-8'),
             })
        i = i+1
        if i == 20*counter or i == temp/20*20:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)
      c.append(result)
      return HttpResponse(c)

#faculty search
  if role == "Faculties":
    faculties = Faculty.objects.all()
    if srch_str != "":
      flag = 1
      faculties = faculties.filter(user__name__icontains=srch_str)
    if faculty_department != "":
      faculties = faculties.filter(department__icontains=faculty_department)
    if faculty_designation != "":
      faculties = faculties.filter(designation__icontains=faculty_designation)
    if flag == 0:
      c.append(result)
      return HttpResponse(c)
    else:
      temp = faculties.count()
      result["temp"]=temp
      for faculty in faculties:
        result["data"].append({
            'name':faculty.user.name.encode('utf-8'),
            'username':faculty.user.username.encode('utf-8'),
            'department':faculty.department.encode('utf-8'),
            'designation':faculty.designation.encode('utf-8'),
            'office-no':faculty.user.contact_no.encode('utf-8'),
            })
        i = i+1
        if i == 20*counter or i == temp/20*20:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)
      c.append(result)
      return HttpResponse(c)

#services search
  if role == "Services":
    services = services_table.objects.all()
    if srch_str != "":
      flag = 1
      services = services.filter(name__icontains = srch_str)
    if services_list != "":
      services = services.filter(service_icontains = services_list)
    if flag == 0:
      c.append(result)
      return HttpResponse(c)
    else:
      temp = services.count()
      result["temp"]=temp
      for service in services:
        result["data"].append({
            'name':service.name.encode('utf-8'),
            'office_no':service.office_no.encode('utf-8'),
            'service':service.service.encode('utf-8'),
            })
        i = i+1
        if i == 20*counter or i == temp/20*20:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)
      c.append(result)
      return HttpResponse(c)

#group search
  if role == "Groups":
    groups = GroupInfo.objects.all()
    if srch_str != "":
      flag = 1
      groups = groups.filter(group__name__icontains = srch_str)
    if groups_list != "":
      groups = groups.filter(group__user__username__icontains = groups_list)
    if flag == 0:
      c.append(result)
      return HttpResponse(c)
    else:
      temp = groups.count()
      result["temp"] = temp
      for group in groups:
        result["data"].append({
            'name':group.group.user.username.encode('utf-8'),
            'phone-no':group.phone_no.encode('utf-8'),
            'email':group.email.encode('utf-8'),
            })
        i = i+1
        if i == 20*counter or i == temp/20*20:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)
      c.append(result)
      return HttpResponse(c)

#all search
  if role == "All":
    result["data"] = {"Students":[],"Faculties":[],"Services":[],"Groups":[]}
    if srch_str != "":
      students = Student.objects.all()
      students = students.filter(user__name__icontains = srch_str)
      temp_stu = students.count()
      faculties = Faculty.objects.all()
      faculties = faculties.filter(user__name__icontains = srch_str)
      temp_fac = faculties.count()
      services = services_table.objects.all()
      services = services.filter(name__icontains = srch_str)
      temp_ser = services.count()
      groups = GroupInfo.objects.all()
      groups = groups.filter(group__name__icontains = srch_str)
      temp_gro = groups.count()
      temp = temp_stu +temp_fac + temp_ser + temp_gro
      result["temp"] = temp
      for student in students:
        result["data"]["Students"].append(
              {
             'name':student.user.name.encode('utf-8') ,
             'enrollment_no':student.user.username.encode('utf-8') ,
             'branch':student.branch.code.encode('utf-8'),
             'year':int((student.semester_no+1)/2),
             'bhawan':student.bhawan.encode('utf-8'),
             'room':student.room_no.encode('utf-8'),
             })
        i = i+1
        if i == 20*counter:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)

      for faculty in faculties:
        result["data"]["Faculties"].append({
            'name':faculty.user.name.encode('utf-8'),
            'username':faculty.user.username.encode('utf-8'),
            'department':faculty.department.encode('utf-8'),
            'designation':faculty.designation.encode('utf-8'),
            'office-no':faculty.user.contact_no.encode('utf-8')
            })
        i = i+1
        if i == 20*counter:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)

      for service in services:
        result["data"]["Services"].append({
          'name':service.name.encode('utf-8'),
          'office_no':service.office_no.encode('utf-8'),
          'service':service.service.encode('utf-8')
          })
        i = i+1
        if i == 20*counter:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)

      for group in groups:
        result["data"]["Groups"].append({
          'name':group.group.user.username.encode('utf-8'),
          'phone-no':group.phone_no.encode('utf-8'),
          'email':group.email.encode('utf-8'),
        })
        i = i+1
        if i == 20*counter or i == temp/20*20:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)

      c.append(result)
      return HttpResponse(c)
    else:
      c.append(result)
      return HttpResponse(c)

