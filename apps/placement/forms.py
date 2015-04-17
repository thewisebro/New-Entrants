import os

from django.contrib.admin.widgets import AdminDateWidget
from django.forms.models import BaseModelFormSet

from core import forms
from core.forms import CKEditorWidget, CurrencyWidget
from nucleus.models import Branch, StudentInfo, Student, Group
from placement import models
from placement import constants as PC
from placement.policy import current_session_year

class Place(forms.ModelForm):
  class Meta:
    model   = models.PlacementPerson
    exclude = ('student', 'no_of_companies_placed', 'status', 'placed_company_category','is_debarred' )

class CompanyForm(forms.ModelForm) :
  def __init__(self, *args, **kwargs):
    super(CompanyForm, self).__init__(*args, **kwargs)
    self.auto_id = '%s'

  #Search for a better method
  contact_person = forms.ModelChoiceField(queryset = models.CPTMember.objects.filter(year = current_session_year()), required=False)
  open_for_disciplines = forms.ModelMultipleChoiceField(queryset=Branch.objects.all().order_by('degree','department'), widget=forms.CheckboxSelectMultiple)
  class Meta :
    model   = models.Company
    fields = ['name',
              'status',
              'place_of_posting',
              'category',
              'latest_date_of_joining',
              'package_ug', 'package_pg', 'package_phd', 'ctc_remark',
              'cgpa_requirement',
              'company_description',
              'contact_person',
              'pre_placement_talk',
              'shortlist_from_resumes',
              'group_discussion',
              'online_test',
              'written_test',
              'paper_based_test',
              'interview_1', 'interview_2', 'interview_3',
              'last_date_of_applying',
              'name_of_post',
              'description_of_post',
              'other_requirements',
              'total_vacancies_for_iitr',
              'website',
              'brochure',
              'sector',
              'open_for_disciplines']
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
  feedback1 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback2 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback3 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback4 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback5 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback6 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
#  feedback7 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
#  feedback8 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))

class Profile(forms.ModelForm):
  class Meta:
    model = StudentInfo
    exclude = ('student', 'nationality', 'marital_status', 'bank_name',
               'bank_account_no', 'height', 'blood_group', 'weight',
               'passport_no', 'nearest_station', 'local_guardian_name',
               'local_guardian_address', 'local_guardian_contact_no',
               'physically_disabled', 'fulltime', 'resident', 'license_no',
               'category', 'home_contact_no', 'birth_date')
  birth_date = forms.DateField(required = True, widget=forms.DateInput(attrs={'class':'iDateField'}))

class EducationalFormset(BaseModelFormSet):
  def clean(self):
    super(EducationalFormset, self).clean()
    courses = []
    for form in self.forms:
      if not form.empty_permitted:
        courseField = form.cleaned_data['course']
        if not courseField in courses:
          courses.append(courseField)
        else:
          raise forms.ValidationError("Same courses is not allowed")
    pass

class Contact(forms.ModelForm):
  email_id = forms.EmailField(required=True)
  personal_contact_no = forms.CharField(required=True, max_length=12, help_text='must be working')
  permanent_contact_no = forms.CharField(required=False, max_length=12, help_text='must be working')
  class Meta:
    model = Student
    exclude = ('user', 'cgpa', 'passout_year')
    read_only_fields = ('semester', 'semester_no', 'branch', 'admission_year')
    required_fields = ('email_id','personal_contact_no')

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

#class CompanycontactForm(forms.ModelForm):
#  when_to_contact = forms.DateField(widget=AdminDateWidget, required=False)
#  class Meta:
#    model = models.CompanyContact
#    exclude = {'contactperson', 'last_updated', 'last_contact'}
#
#class ContactpersonForm(forms.ModelForm):
#  class Meta:
#    model = models.ContactPerson
#
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

    error_css_class = 'control-group error'
    required_css_class = 'required_field'
    error_css_class = error_css_class
    required_css_class = required_css_class

    class Meta:
      model = model_type
      exclude = exclude_list

  return ObjectModelForm(data,**kwargs)

# Following are the forms for new contact manager app

class AssignCoordinatorForm(forms.Form):
  company_coordinator = forms.ModelChoiceField(queryset=Group.objects.get(name='Company Coordinator').user_set.all(), empty_label="None", required=False)

class AddCoordinatorForm(forms.Form):
  student = forms.CharField(widget=forms.TextInput)
  enroll = forms.CharField(widget=forms.HiddenInput(attrs={'id':'enroll'}))

class AddCompanyInfoForm(forms.ModelForm):
  class Meta:
    model = models.CompanyContactInfo

class ContactPersonFormSet(BaseModelFormSet):

  class Meta:
    model = models.ContactPerson
    exclude = {'company_contact',}

class CampusContactFormSet(BaseModelFormSet):

  when_to_contact = forms.DateField(widget=AdminDateWidget, required=False)

  class Meta:
    model = models.CampusContact
    exclude = {'contact_person',}

class CommentsForm(forms.ModelForm):

  class Meta:
    model = models.CompanyContactComments
    exclude = {'date_created', 'campus_contact'}
