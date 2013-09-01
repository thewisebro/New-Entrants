import datetime

from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings

## CKEditor Widget

def filemanager_config(url):
  d = {}
  d['filebrowserBrowseUrl'] = url
  d['filebrowserImageBrowseUrl'] = url
  d['filebrowserWidth'] = 800
  d['filebrowserHeight'] = 500
  return d

class CKEditorWidget(forms.Textarea):
  def __init__(self, attrs={}, config = {}, filemanager_url=''):
    """ config : CKEditor config
        filemanager_url : for user to 'browse server'
        In config : toolbar = 'Basic'/'Standard'/'Full'/'BasicWithImage'
    """
    default = {
      'toolbar': 'Standard',
      'height': 250,
      'width': 900
    }
    default.update(config)
    if filemanager_url:
      default.update(filemanager_config(filemanager_url))
    self.config = default
    return super(CKEditorWidget, self).__init__(attrs)

  class Media:
    js = (
      'ckeditor/ckeditor.js',
    )

  def render(self, name, value, attrs=None):
    rendered = super(CKEditorWidget, self).render(name, value, attrs)
    div = "<div style='height:20px'></div>"
    return rendered+mark_safe(div+
      u"""<script type="text/javascript">
            document.addEventListener('DOMContentLoaded', function() {
              CKEDITOR.replace('%s',%s);
            }, false);
          </script>
      """%(attrs['id'], self.config))


## Date-Time Widgets

class DateTimeMedia:
  js = (
    'jquery/jquery.min.js',
    'jquery/jquery-ui.min.js',
    'jquery/jquery-datetimepicker.js',
    'jquery/jquery-init.js',
  )
  css = {'all':(
    'jquery/smoothness/jquery-ui.min.css',
    'jquery/jquery-datetimepicker.css',
  )}


class DateWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    if isinstance(value, datetime.date):
      value=value.strftime(settings.DATE_INPUT_FORMATS[0])
    if type(attrs) == dict:
      attrs.update({'class': 'iDateField'})
    else:
      attrs = {'class': 'iDateField'}
    return super(DateWidget, self).render(name, value, attrs)

  Media = DateTimeMedia

class TimeWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    if isinstance(value, datetime.time):
      value=value.strftime(settings.TIME_INPUT_FORMATS[0])
    if type(attrs) == dict:
      attrs.update({'class': 'iTimeField'})
    else:
      attrs = {'class': 'iTimeField'}
    return super(TimeWidget, self).render(name, value, attrs)

  Media = DateTimeMedia

class DateTimeWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    if type(attrs) == dict:
      attrs.update({'class': 'iDateTimeField'})
    else:
      attrs = {'class': 'iDateTimeField'}
    return super(DateTimeWidget, self).render(name, value, attrs)

  Media = DateTimeMedia
