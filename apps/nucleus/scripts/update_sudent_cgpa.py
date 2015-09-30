from nucleus.models import *
from placement.models import *
from placement.utils import *

def update_cgpa():
  students = Student.objects.all()
  for stud in students:
    try:
      curr_sem = stud.semester
      course = previous_sem(curr_sem)
      plac_person = PlacementPerson.objects.filter(student=stud)
      edu_details = EducationalDetails.objects.get(student=stud, course=course)
      print 'Edu details CGPA:  %s'%edu_details.cgpa
      stud.cgpa = edu_details.cgpa
      stud.save()
      print 'Student CGPA: %s'%stud.cgpa
    except Exception as e:
      print e
      pass
update_cgpa()
