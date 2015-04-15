import json
import logging
from pprint import pprint
from nucleus.models import Course, User, Batch, Student, Faculty


logging.basicConfig(filename="batch_error.log", format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

with open('apps/lectut/scripts/batch.json') as json_data:
  values = json.load(json_data)
  json_data.close()
#  pprint(values)

  for batch in values:
#    print batch
    code = batch['course_code']
    if Course.objects.filter(code = code).exists():
      course =  Course.objects.get(code = code)
      try:
        batchToAdd = Batch(name = course.id , course = course)
        batchToAdd.save()
      except Exception as e:
        print str(code)+' Batch error '+str(e)
      users = batch['users']
      for user in users:
        try:
          user_object = User.objects.get(username = user)
          student = user_object.student
          batchToAdd.students.add(student)
          batchToAdd.save()
          print 'Successfully added student'
        except Exception as e:
          logging.warning('Student: '+str(user)+'Batch:'+str(code))
          print str(e) + ' student' + str(user)

      faculties = batch['faculties']
      for faculty in faculties:
        try:
          user_object = User.objects.get(username = faculty)
          facultyToAdd = user_object.faculty
          batchToAdd.faculties.add(facultyToAdd)
          batchToAdd.save()
          print 'Successfully added Faculty'
        except Exception as e:
          logging.warning('Faculty:'+str(user)+'batch:'+code)
          print str(e) +' faculty' + str(user)

    else:
      print 'Error in ' + str(code)
    print 'completed batch ' +str(code)
  print 'Over'
