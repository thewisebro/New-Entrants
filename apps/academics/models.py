from core import models
from nucleus.models import Course, Branch, Student


class IEBranchMap(models.Model):
  course = models.ForeignKey(Course)
  branch = models.ForeignKey(Branch)
  semester_nos = models.CommaSeparatedIntegerField(max_length=20, null=True) #comma separated

  def __unicode__(self):
    return self.course.code + ':' + self.branch.code


class IEStudentPreference(models.Model):
  student = models.ForeignKey(Student)
  course = models.ForeignKey(Course)
  priority = models.PositiveIntegerField()

  def __unicode__(self):
    return self.student.user.username + ':' + self.course.code + ':' + self.priority
