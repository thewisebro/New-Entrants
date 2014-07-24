# Create your views here.
from nucleus.models import Student , Faculty
from groups.models import GroupInfo
from peoplesearch.models import services_table
from django.http import HttpResponse

def index(request):
  srch_str = request.GET.get('name','SBI')
  branch = request.GET.get('branch','')
  year = request.GET.get('year','')
  role = request.GET.get('role','Services')
  faculty_department = request.GET.get('faculty_department','')
  faculty_designation = request.GET.get('faculty_designation','')
  services_list = request.GET.get('services_list','')
  groups_list = request.GET.get('groups_list','')
  counter = request.GET.get('counter',0)
  flag=0
  temp=0
  temp_stu=0
  temp_fac=0
  temp_ser=0
  temp_gro=0
  i=0
  result={"role":role,"data":[],"temp":0}
  c=[]
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

