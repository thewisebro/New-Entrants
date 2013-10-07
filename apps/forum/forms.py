from core import forms
from forum.models import Question

class Ask_Question_Form(forms.ModelForm):
  class Meta:
    model = Question
    fields = ['title','description']


