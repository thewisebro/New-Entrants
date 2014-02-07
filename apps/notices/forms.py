from core.forms import ModelForm, ModelChoiceField
from notices.models import Notice
from core import forms

def GenerateNoticeForm(user):
  categories = user.category_set.all()
  class NoticeForm(ModelForm):
    category = forms.ModelChoiceField(queryset=categories, empty_label = None)
    class Meta:
      model = Notice
      fields = ['subject','expire_date','reference', 'content']
  return NoticeForm

class EditForm(ModelForm):
    class Meta:
      model = Notice
      fields = ['subject','expire_date','reference', 'content']
