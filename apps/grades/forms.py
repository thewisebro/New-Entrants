from django import forms
from grades import models
from api.forms import BaseModelForm

class UploadForm(BaseModelForm):
  class Meta:
    model = models.Upload

