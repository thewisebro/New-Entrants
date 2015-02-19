from core import forms
from core.forms import CKEditorWidget, CurrencyWidget
from core.forms import BaseForm, BaseModelForm#, MyModelMultipleChoiceField
from internship import models, constants as IC
from nucleus.models import Branch
from django.contrib.admin import widgets                                       

class CompanyForm(BaseModelForm) :
  latest_date_of_joining = forms.CharField(required= False, widget = forms.DateInput(attrs={'class':'iDateTimeField'}))
  last_date_of_applying = forms.CharField(required= False, widget = forms.DateInput(attrs={'class':'iDateTimeField'}))
  probable_date_of_arrival = forms.CharField(required= False, widget = forms.DateInput(attrs={'class':'iDateTimeField'}))
  open_for_disciplines = forms.ModelMultipleChoiceField(queryset=Branch.objects.filter(graduation__in=('UG','PG')).order_by('degree', 'department'), widget=forms.CheckboxSelectMultiple)
  class Meta :
    model   = models.Company
    exclude = ('year')
    widgets = { #'open_for_disciplines' : forms.CheckboxSelectMultiple,
                'stipend' : CurrencyWidget(choices_whole = IC.PAY_WHOLE_CHOICES, choices_currency = IC.PAY_PACKAGE_CURRENCY_CHOICES, attrs={'class':'iCurrencyField'}),
              }

class NoticeForm(BaseModelForm) :
  class Meta :
    model = models.Notices
    exclude = ('date_of_upload')

class Feedback(BaseForm) :
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


