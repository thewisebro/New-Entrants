from nucleus.models import *
from placement.models import *
from placement.models import PlacementPerson

PlacementPerson.objects.all().update(status='CLS')
btech_students = Student.objects.filter(branch__degree="B.Tech.",semester="UG40", passout_year=None)
idd_students = Student.objects.filter(branch__degree="IDD",semester="UG50", passout_year=None)
barch_students = Student.objects.filter(branch__degree="B.Arch.",semester="UG50",  passout_year=None)
imt_students = Student.objects.filter(branch__degree="IMT",semester="UG50",  passout_year=None)
imsc_students = Student.objects.filter(branch__degree="IMSc",semester="UG50",  passout_year=None)
## Re run this MTech part
mtech_students = Student.objects.filter(branch__degree="M.Tech.", semester="PG20",  passout_year=None)
mca_students = Student.objects.filter(branch__degree='MCA', semester='PG40',  passout_year=None)

success_btech = 0
failure_btech = 0
for i in btech_students:
  try:
    plc_person, created = PlacementPerson.objects.get_or_create(student=i, status='CLS')
    plc_person.status='OPN'
    plc_person.save()
    success_btech += 1
  except:
    print str(i.user.username)+" Failure"
    failure_btech += 1
print "BTech Done"

success_idd = 0
failure_idd = 0
for i in idd_students:
  try:
    plc_person, created = PlacementPerson.objects.get_or_create(student=i, status='CLS')
    plc_person.status='OPN'
    plc_person.save()
    success_idd += 1
  except:
    print str(i.user.username)+" Failure"
    failure_idd += 1
print "IDD Done"

success_barch = 0
failure_barch = 0
for i in barch_students:
  try:
    plc_person, created = PlacementPerson.objects.get_or_create(student=i, status='CLS')
    plc_person.status='OPN'
    plc_person.save()
    success_barch += 1
  except:
    print str(i.user.username)+" Failure"
    failure_barch += 1
print "BArch Done"

success_imt = 0
failure_imt = 0
for i in imt_students:
  try:
    plc_person, created = PlacementPerson.objects.get_or_create(student=i, status='CLS')
    plc_person.status='OPN'
    plc_person.save()
    success_imt += 1
  except:
    print str(i.user.username)+" Failure"
    failure_imt += 1
print "IMT Done"

success_imsc = 0
failure_imsc = 0
for i in imsc_students:
  try:
    plc_person, created = PlacementPerson.objects.get_or_create(student=i, status='CLS')
    plc_person.status='OPN'
    plc_person.save()
    success_imsc += 1
  except:
    print str(i.user.username)+" Failure"
    failure_imsc += 1
print "IMSc Done"

success_mtech = 0
failure_mtech = 0
for i in mtech_students:
   try:
    plc_person, created = PlacementPerson.objects.get_or_create(student=i, status='CLS')
    plc_person.status='OPN'
    plc_person.save()
    success_mtech += 1
   except:
    print str(i.user.username)+" Failure"
    failure_mtech += 1
print "MTech Done"

success_mca = 0
failure_mca = 0
for i in mca_students:
  try:
    plc_person, created = PlacementPerson.objects.get_or_create(student=i, status='CLS')
    plc_person.status='OPN'
    plc_person.save()
    success_mca += 1
  except:
    print str(i.user.username)+" Failure"
    failure_mca += 1
print "MCA Done"
