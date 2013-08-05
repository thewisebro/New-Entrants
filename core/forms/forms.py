from django import forms
from django.template import Context, Template

from crispy_forms.helper import FormHelper

class FormBase(object):
  def __unicode__(self, *args, **kwargs):
    self.helper = FormHelper(self)
    self.helper.disable_csrf = True
    c = Context({'form': self})
    t = Template("{% load crispy_forms_tags %}{% crispy form %}")
    return t.render(c)

class Form(FormBase, forms.Form):
  pass

class ModelForm(FormBase, forms.ModelForm):
  pass
