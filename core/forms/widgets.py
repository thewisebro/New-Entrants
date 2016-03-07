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
  def __init__(self, *args, **kwargs):
    attrs = kwargs.pop('attrs', {})
    cls = attrs.pop('class','')
    attrs.update({'class': cls + ' iDateField'})
    kwargs['attrs'] = attrs
    super(DateWidget, self).__init__(*args, **kwargs)

  def render(self, name, value, attrs=None):
    if isinstance(value, datetime.date):
      value = value.strftime(settings.DATE_INPUT_FORMATS[0])
    return super(DateWidget, self).render(name, value, attrs)

  Media = DateTimeMedia

class TimeWidget(forms.TextInput):
  def __init__(self, *args, **kwargs):
    attrs = kwargs.pop('attrs', {})
    cls = attrs.pop('class','')
    attrs.update({'class': cls + ' iTimeField'})
    kwargs['attrs'] = attrs
    super(TimeWidget, self).__init__(*args, **kwargs)

  def render(self, name, value, attrs=None):
    if isinstance(value, datetime.time):
      value = value.strftime(settings.TIME_INPUT_FORMATS[0])
    return super(TimeWidget, self).render(name, value, attrs)

  Media = DateTimeMedia

class DateTimeWidget(forms.TextInput):
  def __init__(self, *args, **kwargs):
    attrs = kwargs.pop('attrs', {})
    cls = attrs.pop('class','')
    attrs.update({'class': cls + ' iDateTimeField'})
    kwargs['attrs'] = attrs
    super(DateTimeWidget, self).__init__(*args, **kwargs)

  Media = DateTimeMedia


## Select Widgets

class ChosenSelectBase(object):
  def _render(self, *args, **kwargs):
    attrs = kwargs.pop('attrs', {})
    cls = attrs.pop('class','')
    attrs.update({'class': cls + ' chosen-select'})
    kwargs['attrs'] = attrs
    return super(type(self), self).render(*args, **kwargs)

  class Media:
    js = (
      'jquery/jquery.min.js',
      'chosen/chosen.jquery.min.js',
      'jquery/jquery-init.js',
    )
    css = {'all':(
      'chosen/chosen.min.css',
      'jquery/custom.css',
    )}

class ChosenSelect(forms.Select, ChosenSelectBase):
  def render(self, *args, **kwargs):
    return self._render(*args, **kwargs)

class ChosenSelectMultiple(forms.SelectMultiple, ChosenSelectBase):
  def render(self, *args, **kwargs):
    return self._render(*args, **kwargs)


class CurrencyWidget(forms.MultiWidget):
  """
    Renders a complex currency fiels. It renders one text field to get the amount
    and a drop downs to get currency and lacs/thousands.
  """
  def __init__(self, choices_whole=None, choices_currency=None, attrs=None):
    widgets = (forms.TextInput(attrs=attrs),
               forms.Select(choices=choices_whole),
               forms.Select(choices=choices_currency))
    super(CurrencyWidget, self).__init__(widgets, attrs)
  def decompress(self, value):
    if value:
      chunks = filter(lambda s: not s == ' ', value.split(' '))
      return [chunks[0],chunks[-2],chunks[-1]]
    return [None, None, None]
  def value_from_datadict(self, data, files, name):
    values = [widget.value_from_datadict(data, files, name + '_%s' % i) \
                for i, widget in enumerate(self.widgets)]
    try:
      if values[0] :
        amount = values[0].replace(' ','')
        try:
          amount = float(amount)
        except Exception as e:
          amount = 0
        return str(amount) + ' ' + str(values[1]) + ' ' + str(values[2])
      else :
        return ''
    except ValueError:
      return ''
