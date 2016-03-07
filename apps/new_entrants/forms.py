from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, validate_email

from api import model_constants as MC
from nucleus.models import User, Branch, Student
from new_entrants.models import *

def branch_choices():
  t = (('None','None'),)
  for branch in Branch.objects.all():
    t+=(branch.code,branch.name + ' (' + branch.degree + ')'),
  return t

class RegisterForm(forms.Form):
  alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

  name = forms.CharField(label='Name',max_length=100)
  username = forms.CharField(label='Username', max_length=30, validators=[alphanumeric])
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
  password2 = forms.CharField(label='Re-enter Password', widget=forms.PasswordInput)
  branch = forms.ChoiceField(label='Branch', choices=branch_choices())
  email = forms.EmailField(label='Email id', max_length=75, validators=[validate_email])
  fb_link = forms.CharField(label='Facebook link', max_length=200, required=False)
  state = forms.ChoiceField(label='State', choices=MC.STATE_CHOICES)
  hometown = forms.CharField(label='City', max_length=100, required=False)
  phone_no = forms.CharField(label='Contact No', max_length=20, required=False)
  phone_privacy = forms.BooleanField(label='Contact Visibility', initial=True, required=False)
  profile_privacy = forms.BooleanField(label='Profile Visibility', initial=True, required=False)

  def is_valid(self):
    valid = super(RegisterForm, self).is_valid()

    if not valid:
      return valid

    if (self.cleaned_data['password1'] != self.cleaned_data['password2']):
      print "password not same"
      return False

    return True

