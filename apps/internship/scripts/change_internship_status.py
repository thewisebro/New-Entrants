from nucleus.models import *
from internship.models import *
from placement.models import PlacementPerson

InternshipPerson.objects.all().update(status='CLS')
btech_students = Student.objects.filter(branch__degree="B.Tech.",semester="UG30")
idd_students = Student.objects.filter(branch__degree="IDD",semester__in=["UG30","UG40"])
barch_students = Student.objects.filter(branch__degree="B.Arch.",semester__in=["UG30","UG40"])
imt_students = Student.objects.filter(branch__degree="IMT",semester__in=["UG30","UG40"])
imsc_students = Student.objects.filter(branch__degree="IMSc",semester__in=["UG30","UG40"])
## Re run this MTech part
mtech_students = Student.objects.filter(branch__degree="M.Tech.", semester="PG10")

success_btech = 0
failure_btech = 0
for i in btech_students:
  try:
    try:
      intern_person = InternshipPerson.objects.get(student=i)
    except InternshipPerson.DoesNotExist:
      plac_person = PlacementPerson.objects.get_or_create(student=i,status='CLS')
      intern_person = InternshipPerson.objects.create(student=i, status='OPN')
    intern_person.status='OPN'
    intern_person.save()
    success_btech += 1
  except:
    print str(i.user.username)+" Failure"
    failure_btech += 1
print "BTech Done"

success_idd = 0
failure_idd = 0
for i in idd_students:
  try:
    try:
      intern_person = InternshipPerson.objects.get(student=i)
    except InternshipPerson.DoesNotExist:
      plac_person = PlacementPerson.objects.get_or_create(student=i,status='CLS')
      intern_person = InternshipPerson.objects.create(student=i, status='OPN')
    intern_person.status='OPN'
    intern_person.save()
    success_idd += 1
  except:
    print str(i.user.username)+" Failure"
    failure_idd += 1
print "IDD Done"

success_barch = 0
failure_barch = 0
for i in barch_students:
  try:
    try:
      intern_person = InternshipPerson.objects.get(student=i)
    except InternshipPerson.DoesNotExist:
      plac_person = PlacementPerson.objects.get_or_create(student=i,status='CLS')
      intern_person = InternshipPerson.objects.create(student=i, status='OPN')
    intern_person.status='OPN'
    intern_person.save()
    success_barch += 1
  except:
    print str(i.user.username)+" Failure"
    failure_barch += 1
print "BArch Done"

success_imt = 0
failure_imt = 0
for i in imt_students:
  try:
    try:
      intern_person = InternshipPerson.objects.get(student=i)
    except InternshipPerson.DoesNotExist:
      plac_person = PlacementPerson.objects.get_or_create(student=i,status='CLS')
      intern_person = InternshipPerson.objects.create(student=i, status='OPN')
    intern_person.status='OPN'
    intern_person.save()
    success_imt += 1
  except:
    print str(i.user.username)+" Failure"
    failure_imt += 1
print "IMT Done"

success_imsc = 0
failure_imsc = 0
for i in imsc_students:
  try:
    try:
      intern_person = InternshipPerson.objects.get(student=i)
    except InternshipPerson.DoesNotExist:
      plac_person = PlacementPerson.objects.get_or_create(student=i,status='CLS')
      intern_person = InternshipPerson.objects.create(student=i, status='OPN')
    intern_person.status='OPN'
    intern_person.save()
    success_imsc += 1
  except:
    print str(i.user.username)+" Failure"
    failure_imsc += 1
print "IMSc Done"

success_mtech = 0
failure_mtech = 0
for i in mtech_students:
  try:
    try:
      intern_person = InternshipPerson.objects.get(student=i)
    except InternshipPerson.DoesNotExist:
      plac_person = PlacementPerson.objects.get_or_create(student=i,status='CLS')
      intern_person = InternshipPerson.objects.create(student=i, status='OPN')
    intern_person.status='OPN'
    intern_person.save()
    success_mtech += 1
  except:
    failure_mtech += 1
    print str(i.user.username)+" Failure"
print "MTech Done"

