from core import forms
from core.forms import CKEditorWidget, CurrencyWidget
from core.forms import Form, ModelForm
from internship import models, constants as IC
from nucleus.models import Branch

class CompanyForm(ModelForm):
  latest_date_of_joining = forms.CharField(required= False, widget = forms.DateInput(attrs={'class':'iDateField'}))
  last_date_of_applying = forms.CharField(required= False, widget = forms.DateInput(attrs={'class':'iDateTimeField'}))
  probable_date_of_arrival = forms.CharField(required= False, widget = forms.DateInput(attrs={'class':'iDateField'}))
  open_for_disciplines = forms.CompanyMultipleChoiceField(queryset=Branch.objects.filter(graduation__in=('UG','PG')).order_by('degree', 'department'), widget=forms.CheckboxSelectMultiple)
  class Meta:
    model   = models.Company
    exclude = ('year',)
    fields = ['name_of_company',
              'status',
              'address',
              'latest_date_of_joining',
              'stipend', 'stipend_remark',
              'cgpa_requirements',
              'description',
              'designation_of_contact_person',
              'email', 'fax',
              'last_date_of_applying',
              'name_of_contact_person',
              'nature_of_duties', 'name_of_post',
              'no_of_employees',
              'other_requirements',
              'telephone',
              'pre_internship_talk',
              'shortlist_from_resumes',
              'group_discussion',
              'online_test',
              'written_test',
              'paper_based_test',
              'interview_1', 'interview_2', 'interview_3',
              'probable_date_of_arrival',
              'total_vacancies',
              'training_period',
              'turnover',
              'website',
              'brochure',
              'sector',
              'open_for_disciplines']   # Manual listing to change order
    widgets = { #'open_for_disciplines' : forms.CheckboxSelectMultiple,
                'stipend' : CurrencyWidget(choices_whole = IC.PAY_WHOLE_CHOICES, choices_currency = IC.PAY_PACKAGE_CURRENCY_CHOICES, attrs={'class':'iCurrencyField'}),
              }

class NoticeForm(ModelForm) :
  class Meta :
    model = models.Notices
    exclude = ('date_of_upload',)

class Feedback(Form) :
  company_name = forms.ChoiceField(widget=forms.Select)
  feedback1 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback2 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback3 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback4 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback5 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback6 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback7 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))
  feedback8 = forms.CharField(required = False, widget=CKEditorWidget(config={'toolbar':'Basic'}))


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
