from django.db import models
from nucleus.models import Student
from regol.models import CourseDetails
from constants import SEMESTER_CHOICES
from constants import SEASON_CHOICES

class Grade(models.Model):
  person = models.ForeignKey(Student)
  course = models.ForeignKey(CourseDetails,related_name='Grade_course')
  semester = models.CharField(max_length=5)
  grade = models.CharField(max_length=2)
  def __unicode__(self):
    return str(self.course)+' '+str(self.grade)


class Upload(models.Model):
  data = models.FileField(upload_to='grades/')
  semester = models.CharField(max_length=5,choices=SEMESTER_CHOICES)
