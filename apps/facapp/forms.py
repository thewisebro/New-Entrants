from django import forms
from django.forms.widgets import RadioSelect
from django.contrib.auth.forms import AuthenticationForm
from django.forms.models import BaseModelFormSet
from django.utils.safestring import mark_safe
from api import model_constants as MC
# from html_output import _html_output
from django.forms.models import ModelMultipleChoiceField
from django.utils.safestring import mark_safe
# from settings import DATE_INPUT_FORMATS,TIME_INPUT_FORMATS
from facapp.models import *
from core.forms.widgets import CKEditorWidget as CKeditorWidget
import datetime

###################### Custom Fields and Widgets ##################

class DateTimeMedia:
  js = (
    'js/jquery/jquery.min.js',
    'js/jquery/jquery-ui.js',
    'js/jquery/jquery-datetimepicker.js',
    'js/jquery/jquery-init.js',
  )
  css = {'all':(
    'css/smoothness/jquery-ui.css',
    'css/smoothness/custom-jquery-ui.css',
    'css/jquery/jquery-datetimepicker.css',
  )}


class CustomDateWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    if isinstance(value, datetime.date):
      value=value.strftime(DATE_INPUT_FORMATS[0])
    if type(attrs) == dict:
      attrs.update({'class':'iDateField'})
    else:
      attrs = {'class':'iDateField'} 
    return super(CustomDateWidget, self).render(name, value, attrs)
  
  Media = DateTimeMedia

class CustomTimeWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    if isinstance(value, datetime.time):
      value=value.strftime(TIME_INPUT_FORMATS[0])
    if type(attrs) == dict:
      attrs.update({'class':'iTimeField'})
    else:
      attrs = {'class':'iTimeField'} 
    return super(CustomTimeWidget, self).render(name, value, attrs)
  
  Media = DateTimeMedia

###################### Settings for all forms ######################
# def as_div(base_form):
#   """"
#   Returns this form rendered as HTML <div>s
#   """
#   return _html_output(
#       base_form,
#       # html_class_attr has been removed from this line to add clearfix css class to all these divs
#       #normal_row = u'<div%(html_class_attr)s %(html_id_attr)s>%(label)s %(field)s%(help_text)s</div>',
#       normal_row = u'<div class="clearfix" %(html_id_attr)s>%(label)s %(field)s%(help_text)s</div>',
#       error_row = u'%s',
#       row_ender = u'</div>',
#       help_text_html = u'<span class="helptext">%s</span>',
#       errors_on_separate_row = True)

# If the field has errors or is required, then doing 'as_X' will put those fields in the respective classes.
# If field is in both then space separated entries will come.
error_css_class = 'control-group error'
required_css_class = 'required_field'
# In AsDivBaseModelFormSet class, each form is wrapped in a div. This constant defines the CSS class assigned to that div.
formset_form_div_css_class = 'form_itself'

###################### Settings for all forms ######################

class BaseForm(forms.Form):
  """
  This class can be used as a parent class for all Forms. It provides some general functionality that can be used by all forms.
  """

  # Generic form settings:
  # There two variables are provided by Django.
  error_css_class = error_css_class
  required_css_class = required_css_class
  # Make default output of form as_div
  # __unicode__ = as_div

def BaseModelFormFunction(model_type, exclude_list=None, data=None,**kwargs):
  """
    Use this function to create a model form from any model. It creates models with global settings so that all model forms and normaol forms have similar properties.
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

class BaseModelForm(forms.ModelForm):
  """
  This class can be used as a parent class for all Forms. It provides some general functionality that can be used by all forms.
  """
  # Generic form settings:
  # There two variables are provided by Django.
  error_css_class = error_css_class
  required_css_class = required_css_class
  # Make default output of form as_div
  # __unicode__ = as_div

class ConfirmDeleteForm(BaseForm):
  """
  This class can be used to create simple forms with 'Yes' and 'No' options for confirming the deletion of some object.
  """
  choices = forms.fields.ChoiceField(widget=RadioSelect,
      choices=MC.YES_NO_CHOICES, label='')

# class AsDivBaseModelFormSet(BaseModelFormSet) :
#   """
#   Render all the forms present in a FormSet as_div. It also wraps forms in their own divs.
#   """
  # def as_divs(self) :
  #   form_containing_div = '<div class="%s">%s</div>'
  #   forms = u' '.join([form_containing_div%(formset_form_div_css_class,as_div(form)) for form in self])
  #   return mark_safe(u'\n'.join([unicode(self.management_form), forms]))
  # __unicode__ = as_divs

class AsDivList :
  """
  Prints the list enclosed in divs.
  """
  def __init__(self, list, css_class = []) :
    self.__list__ = list
    self.__css_class__ = css_class
  def __unicode__(self) :
    # If the element is a string print it
    if type(self.__list__) == type('') :
      # If css class not defined do not specify class attribute for the div.
      if self.__css_class__ and not self.__css_class__[0] == '':
        return mark_safe(u'<div class="' + self.__css_class__[0] + u'">' + unicode(self.__list__) + u'</div>\n')
      else :
        return mark_safe(u'<div>' + unicode(self.__list__) + u'</div>\n')
    # If list is actually a list recurse over each element and each element must be enclosed in the current div.
    if self.__css_class__ and not self.__css_class__[0] == '':
      ret = u'<div class="' + self.__css_class__[0] + u'">'
    else :
      ret = u'<div>'
    for element in self.__list__ :
      temp_css = self.__css_class__[1:]
      ret = ret + unicode(AsDivList(element, temp_css))
    ret = ret + u'</div>\n'
    return mark_safe(ret)

#For placement and internship to display branches
class MyModelMultipleChoiceField(ModelMultipleChoiceField):
  def label_from_instance(self, branch):
    return mark_safe('<span class="'+branch.department+'">'+branch.degree+' | '+branch.name+'</span>')


class BooksAuthoredForm(BaseModelForm):
  #Next line uncommented as CKEditor being called in template using JS
  books = forms.CharField(label='', widget=CKeditorWidget())
  class Meta:
    model = BooksAuthored
    exclude = ['faculty',]

class RefereedJournalPapersForm(BaseModelForm):
  #Next line uncommented as CKEditor being called in template using JS
  papers = forms.CharField(label='', widget=CKeditorWidget())
  class Meta:
    model = RefereedJournalPapers
    exclude = ['faculty',]

class PhotoUploadForm(BaseForm):
  photo = forms.ImageField()

class ResumeUploadForm(BaseForm):
  resume = forms.FileField()