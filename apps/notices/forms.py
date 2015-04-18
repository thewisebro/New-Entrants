from core.forms import Form, ModelForm, ModelChoiceField
from notices.models import Notice
from core import forms
from django.contrib.admin import widgets

def GenerateNoticeForm(category):
  filemanager_url = str('/notices/browse/'+category.name+'/')
  class NoticeForm(ModelForm):
    class Meta:
      model = Notice
      fields = ['subject','expire_date','reference', 'content']
      widgets = {
        'content': forms.CKEditorWidget(config={
        'width': 900,
        'height': 250,
        'forcePasteAsPlainText': 'true',
        'toolbar': 'Standard',
        },filemanager_url=filemanager_url)
      }
  return NoticeForm

class EditForm(ModelForm):
    class Meta:
      model = Notice
      fields = ['subject','expire_date','reference', 'content']

class DummyForm(Form):
     pass
