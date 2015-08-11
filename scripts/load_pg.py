from nucleus.models import *
from django.contrib.auth.models import Group as GG
import xlrd, xlwt
import time, datetime

def write_row(row_no, row, xl_sheet):
  for i in range(len(row)):
    xl_sheet.write(row_no, i, row[i])

filepath = '../static/excel/PG_1st_year_2015.xlsx'
xl_book = xlrd.open_workbook(filepath)
errorFile = xlwt.Workbook()
errorSheet = errorFile.add_sheet('errors_PG')
done = 0
error = 0
sheet = xl_book.sheet_by_index(0)

group = GG.objects.get(name='Student')
admission_year = 2015
admission_semester = 'A'
ok = False

for i in range(1,sheet.nrows):
  row = sheet.row_values(i)
  try:
    enr_no = str(row[0])
    name = str(row[1])
    gender = str(row[5])
    print row[16]
    try:
      dob = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell(i,16).value,xl_book.datemode)).date()
    except:
      dob = None
    nationality = str(row[17])
    code = str(row[8])
    branch = Branch.objects.get(code = code)
    semester = str(branch.graduation)+'10'
    contact_no = str(row[15])
    if contact_no is None or contact_no is "":
      contact_no = '0'
    email = str(row[14])
    address = str(row[9])+str(row[10])+str(row[11])+str(row[12])
    if len(address)>250:
      address = address[:250]
    pincode = str(row[13])
    if ok is False:
      print "Check below values are mapped properly in column else press CTRL+C"
      print "enr_no " + enr_no
      print "name " + name
      print "gender " + gender
      print "dob " + str(dob)
      print "nation " + nationality
      print "branch " + str(branch)
      print "semester " + str(semester)
      print "contact " + contact_no
      print "email " + email
      print "address " + address
      print "pincode " + pincode
      time.sleep(10)
      ok = True

    user = User.objects.filter(username=enr_no)
    if len(user) == 0 and (enr_no is not None and enr_no is not "") and (name is not None and name is not ""):
      _user = User.objects.create_user(username=enr_no,name=name,password='helloiitr',contact_no=contact_no,birth_date=dob,gender=gender,email=email)
      group.user_set.add(_user)
      person = Student(user=_user, name=name, semester=semester, semester_no=1, branch=branch, admission_year=admission_year, admission_semtype='A')
      person.save()
      info = StudentInfo(student=person,nationality=nationality,permanent_address=address,pincode=pincode)
      info.save()
      print _user.username + ": New User, Person, Info created"
    elif Student.objects.filter(user__username=enr_no).count() == 0:
      person = Student(user=user[0], name=name, semester=semester, semester_no=1, branch=branch, admission_year=admission_year, admission_semtype='A')
      person.save()
      info = StudentInfo(student=person,nationality=nationality,permanent_address=address,pincode=pincode)
      info.save()
      print enr_no + ": User Exist; Person, Info created"
      try:
        user[0].groups.get(name='Student')
      except:
        group.user_set.add(user[0])
        print user[0] + ": group added"
        pass
    elif StudentInfo.objects.filter(student__user__username=enr_no).count() == 0:
      person = Student.objects.get(user__username=enr_no)
      info = StudentInfo(student=person,nationality=nationality,permanent_address=address,pincode=pincode)
      info.save()
      print enr_no + ": User Exist; Person, Info created"
      try:
        user[0].groups.get(name='Student')
      except:
        group.user_set.add(user[0])
        print user[0] + ": group added"
    done += 1
  except KeyError:
    print enr_no, i
    break
  except Exception as e:
    row.append(str(e))
    print str(e)
    error += 1
    print i, enr_no
    try:
      write_row(error-1, row, errorSheet)
    except:
      pass

print "done " + str(done)
print "error " + str(error)
errorFile.save('../static/excel/pg_errors.xlsx')
