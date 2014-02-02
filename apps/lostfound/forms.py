from core import forms

# Ported from oldchanneli.api.apps so that new models do not need to be written
def BaseModelFormFunction(model_type, exclude_list=None, data=None,**kwargs):
  """
    Use this function to create a model form from any model. It creates models with global settings so that all model forms and normaol forms have similar properties.
  """
  # Dynamically create class on the fly. So that only one function can create a generic model form for all models.
  class ObjectModelForm(forms.ModelForm):
    # Generic form settings:
    error_css_class = error_css_class
    required_css_class = required_css_class
    __unicode__ = as_div

    class Meta:
      model = model_type
      exclude = exclude_list

  return ObjectModelForm(data, **kwargs)
