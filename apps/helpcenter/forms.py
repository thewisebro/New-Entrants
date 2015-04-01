from core import forms
from nucleus.constants import *

UserTypeChoices = (
  ('student','Student'),
  ('faculty','Faculty'),
  ('alumni','Alumni'),
  ('other','Other'),
)

class LoginHelpForm(forms.Form):
  user_type = forms.ChoiceField(choices=UserTypeChoices,
      widget=forms.Select(attrs={'onchange':'user_type_changed(this);'}),label='User')
  username = forms.CharField(max_length=10, required=False)
  enrollment_no = forms.IntegerField(required=False, label='Enrollment No')
  email = forms.EmailField(required=True, label='Alternative Email-Id')
  text = forms.CharField(widget=forms.Textarea, label='Describe your problem')

  def clean(self):
    cleaned_data = super(LoginHelpForm,self).clean()
    user_type = cleaned_data.get('user_type')
    username = cleaned_data.get('username')
    enrollment_no = cleaned_data.get('enrollment_no')
    if user_type == 'student' and not (username or enrollment_no):
      raise forms.ValidationError('You must give either Enrollment No or Username')
    return cleaned_data

  def clean_username(self):
    user_type = self.cleaned_data['user_type']
    username = self.cleaned_data['username']
    if (user_type == 'faculty' or user_type == 'other') and not username:
      raise forms.ValidationError('This field is required.')
    return username

def ResponseFormGen(user):
  if user.in_group('Student'):
    choices = map(lambda a:(a,channeli_apps[a]['name']),student_apps)
  elif user.in_group('Faculty'):
    choices = map(lambda a:(a,channeli_apps[a]['name']),faculty_apps)
  else:
    choices = map(lambda a:(a,channeli_apps[a]['name']),other_apps)

  choices = (('','....'),('Channel I','Channel I'))+tuple(choices)

  class ResponseForm(forms.Form):
    app = forms.ChoiceField(choices=choices,required=False)
    text = forms.CharField(widget=forms.Textarea, label='Suggestion')
  return ResponseForm
