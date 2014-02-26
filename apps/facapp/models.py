from core import models
from nucleus.models import Faculty

# Create your models here.

class Section(models.Model):
  title = models.CharField(max_length=200)
  professor = models.ForeignKey(Faculty)
  priority = models.IntegerField()
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  def __unicode__(self):
        return self.title + " of " + str(self.professor.user.username)
