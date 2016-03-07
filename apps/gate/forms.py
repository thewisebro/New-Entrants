from core import forms
from api import model_constants as MC
from gate.constants import *
from django.utils.safestring import mark_safe

class GateForm(forms.Form):
    name = forms.CharField(max_length = MC.TEXT_LENGTH, label = 'Name Of Student',widget=forms.TextInput(attrs={'readonly':'readonly'}))
    employee_id = forms.CharField(max_length = 8, label = 'Employee Id.',widget=forms.TextInput(attrs={'readonly':'readonly'}))
    designation = forms.CharField(label = 'Designation', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    department = forms.CharField(label = 'Department', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    date_of_join = forms.DateField(label = 'Date of Joining IITR', widget=forms.DateInput(attrs={'readonly':'readonly','class':'iDateField'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class':'iDateField'}))
    date_of_joinPos = forms.DateField(required=True,label= 'Date of Joining the present position',widget=forms.DateInput(attrs={'class':'iDateField'}))
    mobile_no = forms.CharField(required=True,max_length=10)
    phone_no_office = forms.CharField()
    phone_no_resi = forms.CharField()
    email = forms.EmailField()
    pay_band_basic = forms.IntegerField(required=False,label = 'Pay Band Basic')
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

    def process(self):
      form = self.cleaned_data

class DeclarationForm(forms.Form):
    accept_1 = forms.BooleanField(required = True,label = mark_safe('None of my close relations (such as WIFE, HUSBAND, SON, DAUGHTER, GRAND-SON, GRAND-DAUGHTER, BROTHER, SISTER, NEPHEW*, NIECE*, UNCLE, AUNT, FIRST COUSIN, SISTER-IN-LAW, BROTHER-IN-LAW, SON-IN-LAW OR DAUGHTER-IN-LAW) OR persons dependent on me OR any one in whom I have a special interest are expected to appear in the Graduate Aptitude Test in Engineering (GATE-2016) - Joint Admission Test for M.Sc. (JAM 2016) to the best of my knowledge.<br/>* Nephew and niece would mean son and daughter of brother or sister of concerned person as well as son and daughter of brother or sister of his/her spouse.'))
    accept_2 = forms.BooleanField(required = True,label = 'If at any later date it comes to my knowledge that any of the above mentioned conditions are violated, I shall bring this fact to your notice immediately in writing.')
    accept_3 = forms.BooleanField(required = True,label = 'I have not written any guide-book or help-book for engineering/science entrance examination.')
    accept_4 = forms.BooleanField(required = True,label = 'I am and shall be in no way directly or indirectly associated wth any coaching activity on remunerative or non-remunerative basis.')
    accept_5 = forms.BooleanField(required = True,label = 'I shall keep my appointment and other matters relating to my participation in GATE-JAM 2016 confidential.')
    def process(self):
      form = self.cleaned_data

