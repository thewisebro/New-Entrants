from core import forms
from grades import models
from core.forms import BaseModelForm

class UploadForm(BaseModelForm):
  class Meta:
    model = models.Upload

