from core import forms
from django.forms import ModelForm, Textarea
from models import *

class FileForm(forms.Form):
  FILE_CHOICES= (
      ('Lecture' , 'Lecture'),
      ('Tutorial' , 'Tutorial'),
      ('Solution' , 'Solution'),
      ('Exam Paper' , 'Exam Paper'),
      ('Question' , 'Question')
      )
  filename=forms.FileField()
  upload_name=forms.CharField()
  upload_type=forms.ChoiceField(choices=FILE_CHOICES)

class TextUpload(forms.Form):
  text=forms.CharField(label='Enter notice' ,widget = forms.Textarea(attrs={'cols': 60, 'rows': 10}))

  def save(self, *args, **kwargs):
         if self.featured:
            self.__class__.objects.all().update(featured = False)
            super(Model, self).save(*args, **kwargs)

