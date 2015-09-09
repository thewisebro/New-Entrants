''' Create Batches out of all available courses '''

from nucleus.models import Course,Batch
count = 0

courses = Course.objects.all()
for course in courses:
  batchToAdd = Batch(name = course.id , course = course)
  batchToAdd.save()
  count +=1

print ' Number of  BAtches added : '+str(count)

