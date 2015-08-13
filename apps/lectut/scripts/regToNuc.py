
from nucleus.models import Course, Batch
from regol.models import CourseDetails

count = 0
reg_courses = CourseDetails.objects.all()
for some_course in reg_courses:
  if not Course.objects.filter(code = some_course.course_code).exists():
    courseToAdd = Course(code = some_course.course_code, name = some_course.course_name, credits = some_course.credits,subject_area = 'Default', semtype = 'A', year = 2015)
    courseToAdd.save()
    batchToAdd = Batch(name = courseToAdd.id , course = courseToAdd)
    batchToAdd.save()
    count +=1
    print str(courseToAdd.code)

print count  

