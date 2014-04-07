from core import forms
from django.forms import ModelForm, Textarea
from models import *

class ImageForm(forms.ModelForm):
          class Meta:
            model = UploadImage

class TextUpload(forms.Form):
  text=forms.CharField(label='Enter notice' ,widget = forms.Textarea(attrs={'cols': 60, 'rows': 10}))

  def save(self, *args, **kwargs):
         if self.featured:
            self.__class__.objects.all().update(featured = False)
            super(Model, self).save(*args, **kwargs)

#<form enctype="multipart/form-data" method="post" action="/foo/">

class UploadFileForm(forms.Form):
  title = forms.CharField(max_lenght=50)
  file = forms.FileField()

