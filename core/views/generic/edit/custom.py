from django.views.generic import edit
from django.forms.models import modelform_factory

from core.forms import ModelForm

def custom_modelform_factory(*args, **kwargs):
  if len(args) == 1:
    return modelform_factory(args[0], ModelForm)
  else:
    return modelform_factory(*args, **kwargs)

edit.model_forms.modelform_factory = custom_modelform_factory
