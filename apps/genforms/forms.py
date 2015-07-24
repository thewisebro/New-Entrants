from django.forms import ModelForm
from genforms.models import *
from django import forms

class LibModelForm(ModelForm):
      class Meta:
          model = LibForm
          fields = ['birth_date', 'permanent_address', 'pincode', 'personal_contact_no', 'fathers_or_guardians_name', 'home_parent_guardian_phone_no','blood_group','valid_till']
          labels = {
                'personal_contact_no' : 'Mobile No. (Self)',
                'home_parent_guardian_phone_no' : 'Home /Parent\'s /Local Guardian\'s Phone No.',
                'fathers_or_guardians_name' : "Father's/ Guardians's Name",
          }

class PicModelForm(ModelForm):
      class Meta:
          model = Pic
          fields = ['pic']
