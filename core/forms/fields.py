from django import forms
from django.utils.safestring import mark_safe
import widgets

class DateField(forms.DateField):
  def __init__(self, *args, **kwargs):
    kwargs.update({'widget': widgets.DateWidget})
    return super(DateField, self).__init__(*args, **kwargs)

class TimeField(forms.TimeField):
  def __init__(self, *args, **kwargs):
    kwargs.update({'widget': widgets.TimeWidget})
    return super(TimeField, self).__init__(*args, **kwargs)

class DateTimeField(forms.DateTimeField):
  def __init__(self, *args, **kwargs):
    kwargs.update({'widget': widgets.DateTimeWidget})
    return super(DateTimeField, self).__init__(*args, **kwargs)

## MultipleChoiceField for displaying branchlist in Placement and Internship
class CompanyMultipleChoiceField(forms.ModelMultipleChoiceField):
  def label_from_instance(self, branch):
    return mark_safe('<span class="'+branch.department+'">'+branch.degree+' | '+branch.name+'</span>')
