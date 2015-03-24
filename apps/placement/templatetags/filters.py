from django import template
from types import BooleanType

register = template.Library()

@register.filter
def get_display(boundField):
  """
  Returns field's data or it's verbose version
  for a field with choices defined.

  Usage::

  {% load filters %}
  {{form.some_field|get_display}}

  Caution :
  Use model.get_FIELD_display() method instead of this filter
  wherever possible.
  """
  data = boundField.value()
  field = boundField.field
  if type(data) == BooleanType :
    if data :
      return 'Yes'
    else :
      return 'No'
  else :
    return hasattr(field, 'choices') and dict(field.choices).get(data,'') or data
