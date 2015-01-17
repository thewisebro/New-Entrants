import os

from django.contrib.admin.widgets import AdminDateWidget

from core import forms
from api.custom_widgets import CKeditorWidget, CurrencyWidget
from nucleus.models import Branch, StudentInfo, Student
from placement import models
from placement import constants as PC
from placement.policy import current_session_year

class Place(forms.ModelForm):
  class Meta:
    model   = models.PlacementPerson
    exclude = ('student', 'no_of_companies_placed', 'status', 'placed_company_category','is_debarred' )

class CompanyForm(forms.ModelForm) :
  #Search for a better method
  contact_person = forms.ModelChoiceField(queryset = models.CPTMember.objects.filter(year = current_session_year()), required=False)
  open_for_disciplines = forms.ModelMultipleChoiceField(queryset=Branch.objects.all().order_by('degree','department'), widget=forms.CheckboxSelectMultiple)
  class Meta :
    model   = models.Company
    exclude = ('year', )
    widgets = {#'open_for_disciplines' : forms.CheckboxSelectMultiple(),
               'package_ug' : CurrencyWidget(choices_whole = PC.PAY_WHOLE_CHOICES,
                                             choices_currency = PC.PAY_PACKAGE_CURRENCY_CHOICES,
                                             attrs={'class':'iCurrencyField'}),
               'package_pg' : CurrencyWidget(choices_whole = PC.PAY_WHOLE_CHOICES,
                                             choices_currency = PC.PAY_PACKAGE_CURRENCY_CHOICES,
                                             attrs={'class':'iCurrencyField'}),
               'package_phd' : CurrencyWidget(choices_whole = PC.PAY_WHOLE_CHOICES,
                                              choices_currency = PC.PAY_PACKAGE_CURRENCY_CHOICES,
                                              attrs={'class':'iCurrencyField'}),
               'latest_date_of_joining' : forms.DateInput(attrs={'class':'iDateField'}),
               'last_date_of_applying' : forms.DateTimeInput(attrs={'class':'iDateTimeField'}),
               'pre_placement_talk' : forms.DateInput(attrs={'class':'iDateField'}),
               }

class NoticesForm(forms.ModelForm) :
  class Meta :
    model   = models.Notices
    exclude = ('date_of_upload',)
  def clean_notice(self) :
    notice = self.cleaned_data['notice']
    # When updating the allowed extensions, update the help_text for the Model as well.
    allowed_extensions = ('txt', 'doc', 'pdf', 'xml', 'xls', 'xlsx')
    extension = notice.name[notice.name.rfind('.') + 1 : ].lower()
    if extension not in allowed_extensions :
      raise forms.ValidationError("File extension '." + extension + "' is not allowed.")
    return notice

class VerifySearch(forms.Form) :
  search_string = forms.CharField(label='Name/Enrollment No')

class Feedback(forms.Form) :
  company = forms.ModelChoiceField(queryset = models.Company.objects.filter(year = current_session_year()).order_by('name'))
  feedback1 = forms.CharField(required = False, widget=CKeditorWidget(toolbar='Basic'))
  feedback2 = forms.CharField(required = False, widget=CKeditorWidget(toolbar='Basic'))
  feedback3 = forms.CharField(required = False, widget=CKeditorWidget(toolbar='Basic'))
  feedback4 = forms.CharField(required = False, widget=CKeditorWidget(toolbar='Basic'))
  feedback5 = forms.CharField(required = False, widget=CKeditorWidget(toolbar='Basic'))
  feedback6 = forms.CharField(required = False, widget=CKeditorWidget(toolbar='Basic'))
#  feedback7 = forms.CharField(required = False, widget=CKeditorWidget(toolbar='Basic'))
#  feedback8 = forms.CharField(required = False, widget=CKeditorWidget(toolbar='Basic'))

class Profile(forms.ModelForm):
  class Meta:
    model = StudentInfo
    exclude = ('student', 'nationality', 'marital_status', 'bank_name',
               'bank_account_no', 'height', 'blood_group', 'weight',
               'passport_no', 'nearest_station', 'local_guardian_name',
               'local_guardian_address', 'local_guardian_contact_no',
               'physically_handicapped', 'fulltime', 'resident', 'license_no',
               'category', 'home_contact_no')
  birth_date = forms.DateField(required = True, widget=forms.DateInput(attrs={'class':'iDateField'}))

class Contact(forms.ModelForm):
  permanent_contact_no = forms.CharField(required=False, max_length=12, help_text='must be working')
  class Meta:
    model = Student
    exclude = ('user', 'photo', 'cgpa', 'passout_year')

class ChangeStatus(forms.Form) :
  enrollment_no = forms.CharField(help_text=' Enter Username / Enrollment No')
  status = forms.ChoiceField(PC.PLACEMENT_STATUS_CHOICES)

class CheckStatus(forms.Form):
  enrollment_no = forms.CharField()

class GenerateRegistrationNo(forms.Form) :
  enrollment_no = forms.CharField(help_text=' Enter Username / Enrollment No')

class ExcelForm(forms.Form):
  excel_file=forms.FileField(required=True , label=u"Upload the excel file")

  def clean_excel_file(self):
      excel_file=self.cleaned_data['excel_file']
      extension = os.path.splitext( excel_file.name )[1]
      if not (extension in PC.IMPORT_FILE_TYPES):
        raise forms.ValidationError( u'%s is not a valid excel file. Please make sure your input file is an excel file' % extension)
      else:
        return excel_file

class CompanycontactForm(forms.ModelForm):
  when_to_contact = forms.DateField(widget=AdminDateWidget, required=False)
  class Meta:
    model = models.CompanyContact
    exclude = {'contactperson', 'last_updated', 'last_contact'}

class ContactpersonForm(forms.ModelForm):
  class Meta:
    model = models.ContactPerson

class AssignCoordinatorForm(forms.Form):
  company_coordinator = forms.ModelChoiceField(queryset=models.CompanyCoordi.objects.all(), empty_label="None", required=False)

class AddCoordinatorForm(forms.Form):
  student = forms.CharField(widget=forms.TextInput)
  enroll = forms.CharField(widget=forms.HiddenInput(attrs={'id':'enroll'}))
  class Meta:
    model = models.CompanyCoordi

class CreateSlotForm(forms.ModelForm):
  start_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
  end_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
  company = forms.CharField(widget=forms.TextInput)

  class Meta:
    model = models.CompanySlot

class EditSlotForm(forms.ModelForm):
  start_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M','%d-%m-%Y %H:%M'])
  end_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M', '%d-%m-%Y %H:%M'])
  company = forms.CharField(widget=forms.TextInput)
  status = forms.BooleanField(initial=True)
  class Meta:
    model = models.CompanySlot

class AddShortlistForm(forms.Form):
  student = forms.CharField(widget=forms.Textarea)
  company = forms.CharField(widget=forms.TextInput)

def BaseModelFormFunction(model_type, exclude_list=None, data=None,**kwargs):
  """
    Use this function to create a model form from any model. It creates models with global settings so that all model forms and normaol forms have similar properties.
  """
  # Dynamically create class on the fly. So that only one function can create a generic model form for all models.
  class ObjectModelForm(forms.ModelForm):
    # Generic form settings:
    error_css_class = error_css_class
    required_css_class = required_css_class

    class Meta:
      model = model_type
      exclude = exclude_list

  return ObjectModelForm(data,**kwargs)

