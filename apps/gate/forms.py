from core import forms
from api import model_constants as MC
from gate.constants import *


class GateForm(forms.Form):
    name = forms.CharField(max_length = MC.TEXT_LENGTH, label = 'Name Of Student',widget=forms.TextInput(attrs={'readonly':'readonly'}))
    employee_id = forms.CharField(max_length = 8, label = 'Employee Id.',widget=forms.TextInput(attrs={'readonly':'readonly'}))
    designation = forms.CharField(label = 'Designation', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    department = forms.CharField(label = 'Department', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    date_of_join = forms.CharField(label = 'Date of Joining IITR', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    date_of_birth = forms.CharField(label = 'Date of Birth', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    date_of_joinPos = forms.CharField(label= 'Date of Joining the present position')
    mobile_no = forms.CharField()
    phone_no_office = forms.IntegerField(required=False)
    phone_no_resi = forms.IntegerField(required=False)
    email = forms.EmailField()
    grade_pay = forms.IntegerField(required=False,label = 'Present Grade Pay')
    income = forms.IntegerField(label='Annual Income')
    home_address = forms.CharField(label = 'Permanent address')
    height = forms.IntegerField(required=False,label='Height(cms)')
    weight = forms.IntegerField(required=False,label='Weight(kgs)')
    age = forms.IntegerField(required=False,label='Age(yrs)')
    nominee = forms.CharField(label = 'Nominee Name')
    nominee_relation = forms.CharField(label = 'Relation with Nominee')
    pref1 = forms.ChoiceField(choices=WEEKS,label='1st preference')
    pref2 = forms.ChoiceField(choices=WEEKS,label='2nd preference')
    city1 = forms.ChoiceField(choices=CITIES,label='First Choice')
    city2 = forms.ChoiceField(choices=CITIES,label='Second Choice')
    city3 = forms.ChoiceField(choices=CITIES,label='Third Choice')
    city4 = forms.ChoiceField(choices=CITIES,label='Fourth Choice')
    city5 = forms.ChoiceField(choices=CITIES,label='Fifth Choice')
    city6 = forms.ChoiceField(choices=CITIES,label='Sixth Choice')
    account_no = forms.IntegerField(label = 'Salary Account no.')

    def process(self):
      form = self.cleaned_data


