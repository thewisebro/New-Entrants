
from core import forms

#<form enctype="multipart/form-data" method="post" action="/foo/">

class UploadFileForm(forms.Form):
  title = forms.CharField(max_lenght=50)
  file = forms.FileField()

