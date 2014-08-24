from core import forms
from core.forms.mixins import FormMixin
from nucleus.models import StudentUserInfo

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
