from core import forms
from django.forms import ModelForm, Textarea
from models import *

MAX_FILE_SIZE = 524

class FileForm(forms.Form):
  FILE_CHOICES= (
      ('Lec' , 'Lecture'),
      ('Tut' , 'Tutorial'),
      ('Sol' , 'Solution'),
      ('ExP' , 'Exam Paper'),
      ('Que' , 'Question')
      )
  filename=forms.FileField()
  upload_name=forms.CharField()
  upload_type=forms.ChoiceField(choices=FILE_CHOICES)

  def __init__(self,userType,*args,**kwargs):
    super(FileForm, self).__init__(*args, **kwargs)
    if userType=='1':
      self.fields['privacy']=forms.BooleanField()

'''  def clean(self):
    filename = self.cleaned_data.get("filename")
    import pdb; pdb.set_trace#();
    upload_name = self.cleaned_data.get("upload_name")
    if filename:
      if not upload_name:
#raise forms.ValidationError("Enter name of the file")
        msg="Enter name of the file"
      elif filename._size>MAX_FILE_SIZE:
        raise forms.ValidationError("The file size should be less than 5MB")
    else:
      raise forms.ValidationError("Please choose a file before submitting")
    return self.cleaned_data
'''
class TextForm(forms.Form):
  text=forms.CharField(label='Enter notice' ,widget = forms.Textarea(attrs={'cols': 60, 'rows': 10}))

  def save(self, *args, **kwargs):
         if self.featured:
            self.__class__.objects.all().update(featured = False)
            super(Model, self).save(*args, **kwargs)

