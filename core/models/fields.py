from django.db import models

from core import forms

class CKEditorField(models.TextField):
  def __init__(self, *args, **kwargs):
    """ arguments config,filemanager_url can be passed here
        for the same use as of CKEditorWidget.
    """
    self.config = kwargs.pop('config', {})
    self.filemanager_url = kwargs.pop('filemanager_url', '')
    super(CKEditorField, self).__init__(*args, **kwargs)

  def formfield(self, **kwargs):
    defaults = {
      'form_class': forms.CharField,
      'widget': forms.CKEditorWidget(config=self.config, filemanager_url=self.filemanager_url)
    }
    defaults.update(kwargs)
    return super(CKEditorField, self).formfield(**defaults)

class DateField(models.DateField):
  def formfield(self, *args, **kwargs):
    kwargs.update({'widget': forms.DateWidget})
    return super(DateField, self).formfield(*args, **kwargs)

class TimeField(models.TimeField):
  def formfield(self, *args, **kwargs):
    kwargs.update({'widget': forms.TimeWidget})
    return super(TimeField, self).formfield(*args, **kwargs)

class DateTimeField(models.DateTimeField):
  def formfield(self, *args, **kwargs):
    kwargs.update({'widget': forms.DateTimeWidget})
    return super(TimeField, self).formfield(*args, **kwargs)
