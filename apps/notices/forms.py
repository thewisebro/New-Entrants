from core.forms import ModelForm, ModelChoiceField
from notices.models import Notice
from core import forms

def GenerateNoticeForm(user):
  filemanager_url = str('/events/browse/'+calendar.name+'/')
  categories = user.category_set.all()
  class NoticeForm(ModelForm):
    category = forms.ModelChoiceField(queryset=categories, empty_label = None)
    class Meta:
      model = Notice
      fields = ['subject','expire_date','reference', 'content']
      widgets = {
        'description': forms.CKEditorWidget(config={
        'toolbar': 'BasicWithImage',
        'width': 800,
        'height': 250,
        'forcePasteAsPlainText': 'true'
        },filemanager_url=filemanager_url)
      }
  return NoticeForm

class EditForm(ModelForm):
    class Meta:
      model = Notice
      fields = ['subject','expire_date','reference', 'content']
