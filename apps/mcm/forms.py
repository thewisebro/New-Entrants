from core import forms
from api import model_constants as MC
from mcm.constants import *

other_scholarship_options= (
   ('MCM','Merit Cum Means Scholarship'),
     ('Loan/Aid','Student loan Aid Scholarship'),
    ('Student Grant', 'Student Grant'),
   ('others','Others' ))

class McmForm(forms.Form):
    name = forms.CharField(max_length = MC.TEXT_LENGTH, label = 'Name Of Student')
    branch = forms.CharField()
    scholar_type=forms.ChoiceField(choices=SCHOLAR_TYPE)
    air = forms.IntegerField(label = 'All India Rank In IIT-JEE')
    semester = forms.ChoiceField(choices=MC.SEMESTER_CHOICES)
    unfair_means = forms.BooleanField(required = False, label = 'Punished for unfair means' )
    fathers_name = forms.CharField(label = 'Father\'s name')
    fathers_occupation = forms.CharField(label = 'Father\'s Occupation')
    home_address = forms.CharField(label = 'Permanent address')
    family_income = forms.IntegerField(label = 'Family Income')
    other_scholarship = forms.BooleanField( required = False, label = 'Entitled to any other scholarship')
    payment_choice=forms.ChoiceField(choices=PAYMENT_CHOICE, required= False)
    bhawan = forms.ChoiceField(choices = MC.BHAWAN_CHOICES ,label = 'Bhawan name')
    room_no = forms.CharField()
    mobile_no = forms.CharField()
    email = forms.EmailField()
    bank_name = forms.ChoiceField(choices=MC.BANK_NAME)
    account_no = forms.IntegerField()
    category = forms.ChoiceField(choices=MC.CATEGORY_CHOICES)
    graduation = forms.ChoiceField(choices=MC.GRADUATION_CHOICES)

    def process(self):
      form = self.cleaned_data

class StudentLoanAidForm(forms.Form):
    name = forms.CharField(max_length = MC.TEXT_LENGTH, label = 'Name Of Student',widget=forms.TextInput(attrs={'readonly':'readonly'}))
    enroll_no = forms.CharField(max_length = 8, label = 'Enrollment No.',widget=forms.TextInput(attrs={'readonly':'readonly'}))
    branch = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    semester = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    graduation = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    category = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    sgpa = forms.CharField(label = 'SGPA(Last Semester)', required = False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    cgpa = forms.CharField(label = 'CGPA', required = False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    fathers_name = forms.CharField(label = 'Father\'s name')
    fathers_occupation = forms.CharField(label = 'Father\'s Occupation')
    home_address = forms.CharField(label = 'Permanent address')
    bhawan = forms.ChoiceField(choices = MC.BHAWAN_CHOICES ,label = 'Bhawan name')
    room_no = forms.CharField()
    bank_name = forms.ChoiceField(choices=MC.BANK_NAME, label = 'Student\'s Bank Name')
    account_no = forms.IntegerField(label = 'Student\'s Account no.')
    guardians_name = forms.CharField(max_length = 20, required = False)
    guardians_occupation = forms.CharField(max_length = 20, required = False)
    guardians_address = forms.CharField(required = False)
    guardians_pan_no = forms.CharField(max_length = 10, required = False)
    fathers_pan_no = forms.CharField(max_length = 10, required = False)
    mothers_pan_no = forms.CharField(max_length = 10, required = False)
    fathers_income = forms.IntegerField(required = False)
    mothers_name = forms.CharField(label = 'Mother\'s name', required = False)
    guardians_income = forms.IntegerField(required = False)
    mothers_income = forms.IntegerField(required = False)
    mothers_occupation = forms.CharField(label = 'Mother\'s Occupation', required = False)
    home_address = forms.CharField(label = 'Permanent address')
    other_scholarship_details = forms.CharField( required = False)
    previous_aid_amount = forms.IntegerField( required = False)
    previous_aid_session = forms.CharField( required = False)
    work_bhawan_details = forms.CharField(required = False)

    def process(self):
      form = self.cleaned_data

class MCMForm(forms.Form):
    name = forms.CharField(max_length = MC.TEXT_LENGTH, label = 'Name Of Student',widget=forms.TextInput(attrs={'readonly':'readonly'}))
    enroll_no = forms.CharField(max_length = 8, label = 'Enrollment No.',widget=forms.TextInput(attrs={'readonly':'readonly'}))
    branch = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    semester = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    scholar_type=forms.ChoiceField(choices=SCHOLAR_TYPE)
    graduation = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    category = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    mobile_no = forms.CharField()
    email = forms.EmailField()
    sgpa = forms.CharField(label = 'SGPA(Last Semester)', required = False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    cgpa = forms.CharField(label = 'CGPA', required = False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    air = forms.IntegerField(required=False,label = 'All India Rank In IIT-JEE')
    unfair_means = forms.BooleanField(required = False, label = 'Punished for unfair means' )
    fathers_name = forms.CharField(label = 'Father\'s name')
    fathers_occupation = forms.CharField(label = 'Father\'s Occupation')
    family_income = forms.IntegerField(label='Family\'s Income')
    home_address = forms.CharField(label = 'Permanent address')
    bhawan = forms.ChoiceField(choices = MC.BHAWAN_CHOICES ,label = 'Bhawan name')
    room_no = forms.CharField()
    bank_name = forms.ChoiceField(choices=MC.BANK_NAME, label = 'Student\'s Bank Name')
    account_no = forms.IntegerField(label = 'Student\'s Account no.')
    other_scholarship_details = forms.CharField( required = False)
    payment_choice=forms.ChoiceField(choices=PAYMENT_CHOICE, widget=forms.RadioSelect(), required=False)

    def process(self):
      form = self.cleaned_data


