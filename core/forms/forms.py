from django import forms
from django.template import Context, Template

from crispy_forms.helper import FormHelper

class FormBase(object):
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper(self)

  def uniform(self, *args, **kwargs):
    self.helper.disable_csrf = True
    self.helper.form_tag = False
    c = Context({'form': self})
    t = Template("{% load crispy_forms_tags %}{% crispy form %}")
    return t.render(c)

  class Media:
    js = (
      'jquery/jquery.min.js',
      'uni_form/uni-form.jquery.js',
      'jquery/jquery-init.js',
    )
    css = {'all':(
      'jquery/smoothness/jquery-ui.min.css',
      'uni_form/uni-form.css',
      'uni_form/default.uni-form.css',
      'jquery/custom.css',
    )}


class Form(forms.Form, FormBase):
  def __init__(self, *args, **kwargs):
    super(Form, self).__init__(*args, **kwargs)
    FormBase.__init__(self, *args, **kwargs)

class ModelForm(forms.ModelForm, FormBase):
  def __init__(self, *args, **kwargs):
    super(ModelForm, self).__init__(*args, **kwargs)
    FormBase.__init__(self, *args, **kwargs)
