from django import forms
from buysell.html_output import _html_output

class detailsForm(forms.Form):
  item_name = forms.CharField()
  cost = forms.IntegerField()
  status = forms.CharField()
  detail = forms.CharField()
  phone_number = forms.CharField()
  email = forms.EmailField()

class requestedForm(forms.Form):
  item_name = forms.CharField()
  item_description = forms.CharField()
  should_cost_at_most = forms.IntegerField()
  phone_number = forms.CharField()
  email = forms.EmailField()

# For BaseModelFormFunction
def as_div(base_form):
  return _html_output(
      base_form,
      normal_row = u'<div class="clearfix" %(html_id_attr)s>%(label)s %(field)s%(help_text)s</div>',
      error_row = u'%s',
      row_ender = u'</div>',
      help_text_html = u'<span class="helptext">%s</span>',
      errors_on_separate_row = True)

# Ported from oldchanneli.api.apps so that new models do not need to be written
def BaseModelFormFunction(model_type, exclude_list=None, data=None,**kwargs):
  error_css_class_name = 'control-group error'
  required_css_class_name = 'required_field'
  class ObjectModelForm(forms.ModelForm):
    error_css_class = error_css_class_name
    required_css_class = required_css_class_name
    __unicode__ = as_div

    class Meta:
      model = model_type
      exclude = exclude_list
  return ObjectModelForm(data, **kwargs)
