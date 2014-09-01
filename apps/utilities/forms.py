from django.db.models import Q

from core import forms
from core.forms.mixins import FormMixin
from nucleus.models import StudentUserInfo
from events.models import Calendar, EventsUser


class ProfileFormPrimary(forms.ModelForm, FormMixin):
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
    one_time_editable_fields = ('first_name', 'category', 'gender', 'birth_date')
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


class EmailForm(forms.Form):
  email = forms.EmailField()

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
