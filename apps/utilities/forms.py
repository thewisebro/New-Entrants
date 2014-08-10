from core import forms
from core.forms.mixins import FormMixin
from nucleus.models import StudentUserInfo

class ProfileForm(forms.ModelForm, FormMixin):
  class Meta:
    model = StudentUserInfo
    fields = [
      'username',
      'name',
      'branch',
      'first_name',
      'photo',
      'category',
      'gender',
      'birth_date',
      'email',
      'contact_no',
      'bhawan',
      'room_no',
      'bank_name',
      'bank_account_no',
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
      'nationality',
      'marital_status',
      'passport_no',
      'nearest_station',
      'blood_group',
      'physically_disabled',
      'fulltime',
      'resident',
      'license_no'
    ]
    read_only_fields = ('username', 'name', 'branch')
    required_fields = ('first_name', 'category', 'gender', 'birth_date')
    one_time_editable_fields = ('first_name', 'category', 'gender', 'birth_date')
    labels = {
      'username': 'Enrollment No',
    }
