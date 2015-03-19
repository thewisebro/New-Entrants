from django import forms
from django.forms.widgets import RadioSelect
from core.forms import BaseForm, ModelForm
from facapp.models import *
# from api.custom_widgets import CKeditorWidget

class BooksAuthoredForm(ModelForm):
  #Next line uncommented as CKEditor being called in template using JS
  #books = forms.CharField(label='', widget=CKeditorWidget(toolbar='Basic',height=300))
  class Meta:
    model = BooksAuthored
    exclude = ['faculty',]

class RefereedJournalPapersForm(ModelForm):
  #Next line uncommented as CKEditor being called in template using JS
  #papers = forms.CharField(label='', widget=CKeditorWidget(toolbar='Basic',height=300))
  class Meta:
    model = RefereedJournalPapers
    exclude = ['faculty',]

class PhotoUploadForm(BaseForm):
  photo = forms.ImageField()

class ResumeUploadForm(BaseForm):
  resume = forms.FileField()



# If the field has errors or is required, then doing 'as_X' will put those fields in the respective classes.
# If field is in both then space separated entries will come.
error_css_class = 'control-group error'
required_css_class = 'required_field'
# In AsDivBaseModelFormSet class, each form is wrapped in a div. This constant defines the CSS class assigned to that div.
formset_form_div_css_class = 'form_itself'

###################### Settings for all forms ######################

def BaseModelFormFunction(model_type, exclude_list=None, data=None,**kwargs):
  """
    Use this function to create a model form from any model.
    It creates models with global settings so that all model forms and normal forms have similar properties.
  """
  # Dynamically create class on the fly. So that only one function can create a generic model form for all models.
  class ObjectModelForm(forms.ModelForm):
    # Generic form settings:
    error_css_class = error_css_class
    required_css_class = required_css_class
    # __unicode__ = as_div

    class Meta:
      model = model_type
      exclude = exclude_list

  return ObjectModelForm(data,**kwargs)

class ConfirmDeleteForm(BaseForm):
  """
  This class can be used to create simple forms with 'Yes' and 'No' options for confirming the deletion of some object.
  """
  choices = forms.fields.ChoiceField(widget=RadioSelect,
      choices=MC.YES_NO_CHOICES, label='')

