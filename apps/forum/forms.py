from core import forms

class Ask_Question_Form(forms.Form):
  title = forms.CharField(max_length=100)
  description = forms.CharField()

