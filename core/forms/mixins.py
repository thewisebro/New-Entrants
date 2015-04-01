import datetime

from django import forms
from django.conf import settings

def _get_cleaner(form, field):
    def clean_field():
         return getattr(form.instance, field, None)
    return clean_field

def  _get_to_python(form, field):
    def to_python(value):
      return getattr(form.instance, field, None)
    return to_python

class ReadOnlyTextInput(forms.TextInput):
  def __init__(self, attrs=None, choices=None):
    self.choices = choices
    super(ReadOnlyTextInput, self).__init__(attrs=attrs)

  def render(self, name, value, attrs):
    if self.choices:
      choices_dict = dict(self.choices)
      value = choices_dict.get(value, value)
    if isinstance(value, datetime.date):
      value = value.strftime(settings.DATE_INPUT_FORMATS[0])
    if isinstance(value, datetime.time):
      value = value.strftime(settings.TIME_INPUT_FORMATS[0])
    return super(ReadOnlyTextInput, self).render(name, value, attrs)

class FormMixin(forms.BaseForm):
    def __init__(self, *args, **kwargs):
        super(FormMixin, self).__init__(*args, **kwargs)
        if isinstance(self, forms.ModelForm) and self.instance and self.instance.pk:
          for field in self._read_only_fields():
              model_field = dict(map(lambda k:(k.name,k),
                    self.instance._meta.fields))[field]
              self.fields[field].widget = ReadOnlyTextInput(attrs={
                  'readonly':'readonly'}, choices=model_field.choices)
              setattr(self, "clean_" + field, _get_cleaner(self, field))
              setattr(self.fields[field], "to_python", _get_to_python(self, field))

    def _read_only_fields(self):
      read_only_fields = []
      if hasattr(self.Meta, 'read_only_fields'):
        read_only_fields += self.Meta.read_only_fields
      if hasattr(self.Meta, 'one_time_editable_fields'):
        ote_fields = self.Meta.one_time_editable_fields
        for f in ote_fields:
          if getattr(self.instance, f, None):
            read_only_fields.append(f)
      return read_only_fields
