from django.db import models
from core.forms import ModelForm
class Upload_Notice(models.Model):
  subject = models.CharField(max_length=200)
  expire_date = models.DateTimeField()
  reference_no = models.CharField(max_length=100)
  copy_to = models.ManyToManyField('Category')

class Category(models.Model):
  main_category = models.CharField(max_length=100,choices =(('Plc', 'Placement'),('Aut', 'Authorities'),('Dep', 'Departments'),('Bwn', 'Bhawans'),('All', 'All')))
  name = models.CharField(max_length=100)
  code = models.CharField(max_length=100)

class Upload_NoticeForm(ModelForm):
  class Meta:
    model = Upload_Notice
    fields = '__all__'

