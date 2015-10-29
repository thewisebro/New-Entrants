from nucleus.models import Batch, Course, User, Student, Faculty
from regol.models import RegisteredCourses, CourseDetails

count = 0
reg_courses = RegisteredCourses.objects.filter(semester_type = 'A').filter(year=2015).filter(cleared_status='CUR').all()
for some_course in reg_courses:
  try:
    some_student = some_course.student
    code = str(some_course.course_details.course_code)
    course = Course.objects.get(code = code)
    batch = Batch.objects.get(course = course)
    if not some_student in batch.students.all():
      batch.students.add(some_student)
      count+=1
      print 'code'+str(some_course.course_details.course_code)
  except Exception as e:
    print e

print 'Number of students added'+str(count)
