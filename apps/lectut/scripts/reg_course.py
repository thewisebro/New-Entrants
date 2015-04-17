import json
import logging
from nucleus.models import Course,User,Batch

#logging.basicConfig(filename="batch_error.log", format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

with open('apps/lectut/scripts/reg1.json') as json_data:
  values = json.load(json_data)
  total_len = len(values)
  json_data.close()
  success,batch_creates,student_added = 0,0,0

  for entry in values:
    try:
      user = User.objects.get(username = entry['username'])
      course_code = entry['course_code']
      student = user.student
      if Course.objects.filter(code = course_code).exists():
        course = Course.objects.get(code = course_code)
        if Batch.objects.filter(course = course).exists():
          checker = False
          batches = Batch.objects.filter(course = course).all()
          for batch in batches:
            if student in batch.students.all():
              checker = True

          if not checker:
            batches[0].students.add(student)
            student_added +=1 
        else:
          batchToAdd = Batch(name = course.id , course = course)
          batchToAdd.save()
          batch_creates +=1
          batchToAdd.students.add(student)
          print 'Batch created'
    except:
      pass
  print 'Success: '+ str(success)
  print 'Batches created '+ str(batch_creates)
  print 'Students added' +str(batch_creates + student_added)
