from django.db.models import Q

from core import forms
from core.forms.mixins import FormMixin
from nucleus.models import StudentUserInfo, User
from events.models import Calendar, EventsUser
from notices.models import NoticeUser
from notices.constants import *

class ProfileFormCleanMixin(forms.Form):
  "Mixin form for cleaning fields"
  def clean_first_name(self):
    first_name = self.cleaned_data['first_name']
    first_name = first_name.strip()
    name = self.instance.name
    first_name_chunks = set(map(lambda a:a, first_name.lower().split(' ')))
    name_chunks = set(map(lambda a:a, name.lower().split(' ')))
    if first_name_chunks.issubset(name_chunks) and\
          (not len(first_name_chunks) == len(name_chunks) or
          len(name_chunks) == 1):
      if first_name.lower() == first_name or first_name.upper() == first_name:
        first_name = first_name.title()
    else:
      raise forms.ValidationError(
        'First name is not valid. It should be subname of your full name.')
    return first_name


class GenProfileForm(forms.ModelForm, FormMixin, ProfileFormCleanMixin):
  class Meta:
    model = User
    fields = [
      'username',
      'first_name',
      'gender',
      'birth_date',
      'email',
      'contact_no',
    ]
    read_only_fields = ['username']
    required_fields = ('first_name', 'gender', 'birth_date')
    one_time_editable_fields = ('first_name', 'gender', 'birth_date', 'email')


class ProfileFormPrimary(forms.ModelForm, FormMixin, ProfileFormCleanMixin):
  class Meta:
    model = StudentUserInfo
    fields = [
      'username',
      'first_name',
      'semester_no',
      'admission_year',
      'admission_semtype',
      'category',
      'gender',
      'birth_date',
      'email',
      'contact_no',
      'bhawan',
      'room_no',
      'bank_name',
      'bank_account_no',
    ]
    read_only_fields = ('username', 'semester_no',
                        'admission_year', 'admission_semtype')
    required_fields = ('first_name', 'category', 'gender', 'birth_date')
    one_time_editable_fields = ('first_name', 'category', 'gender', 'birth_date',
                        'email')
    labels = {
      'username': 'Enrollment No',
      'semester_no': 'Semester',
    }

class ProfileFormGuardian(forms.ModelForm):
  class Meta:
    model = StudentUserInfo
    fields = [
      'fathers_name',
      'fathers_occupation',
      'fathers_office_address',
      'fathers_office_address',
      'fathers_office_phone_no',
      'mothers_name',
      'permanent_address',
      'home_contact_no',
      'state',
      'city',
      'pincode',
      'local_guardian_name',
      'local_guardian_address',
      'local_guardian_contact_no',
    ]

class ProfileFormExtra(forms.ModelForm):
  class Meta:
    model = StudentUserInfo
    fields = [
      'nationality',
      'marital_status',
      'passport_no',
      'nearest_station',
      'blood_group',
      'physically_disabled',
      'resident',
      'license_no',
    ]


class ChangePasswordForm(forms.Form):
  password = forms.CharField(label='Current Password', widget=forms.PasswordInput, required=True, min_length=4)
  password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, required=True, min_length=4)
  password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True, min_length=4)


class ChangePasswordFirstYearForm(forms.Form):
  password1 = forms.CharField(label='Enter New Password', widget=forms.PasswordInput, required=True, min_length=4)
  password2 = forms.CharField(label='Enter Again', widget=forms.PasswordInput, required=True, min_length=4)

class PasswordCheckForm(forms.Form):
  password = forms.CharField(label='Enter Password', widget=forms.PasswordInput, required=True)

class EmailForm(forms.ModelForm, FormMixin):
  class Meta:
    model = User
    fields = ('email',)
    required_fields = ('email',)
    one_time_editable_fields = ('email',)

def EventsSubscribeFormGen(user):
  class EventsSubscribeForm(forms.ModelForm):
    class Meta:
      model = EventsUser
      exclude = ('user',)
      widgets = {
        'calendars' : forms.CheckboxSelectMultiple,
      }
    def __init__(self, *args, **kwargs):
      super(EventsSubscribeForm, self).__init__(*args, **kwargs)
      self.fields['calendars'].queryset = Calendar.objects.exclude(Q(cal_type = 'PRI'),~Q(name = user.username))
      self.fields['email_subscribed'].widget.attrs = {'onchange':'subscription_checkbox_clicked(this)'}
  return EventsSubscribeForm

class NoticesSubscribeForm(forms.ModelForm):
  categories = forms.MultipleChoiceField(choices=MAIN_CATEGORIES_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
  class Meta:
    model = NoticeUser
    fields = ('subscribed',)
  def __init__(self, *args, **kwargs):
    super(NoticesSubscribeForm, self).__init__(*args, **kwargs)
    self.fields['subscribed'].widget.attrs = {'onchange':'notice_subscription_checkbox_clicked(this)'}

class UserEmailForm(forms.Form):
  email = forms.EmailField(label='Email', required = True)

class PasswordResetForm(forms.Form):
  password1 = forms.CharField(label='Enter New Password', widget=forms.PasswordInput, required=True, min_length=4)
  password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True, min_length=4)

class PasswordResetRequestForm(forms.Form):
  email = forms.EmailField(label="Primary email", required=True)
