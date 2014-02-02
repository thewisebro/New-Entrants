from django.contrib.admin import widgets

from core import forms
from events.models import Event
from events.constants import EVENT_TYPE_CHOICES

def EventFormGenerator(calendar, exclude_event_type=False):
  filemanager_url = str('/events/browse/'+calendar.name+'/')
  excludes = ('calendar', 'uploader', 'email_sent')
  if exclude_event_type:
    excludes += ('event_type',)

  class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
      super(EventForm, self).__init__(*args, **kwargs)
      if not exclude_event_type and calendar.cal_type == 'PRI':
        self.fields['event_type'].choices = (
          ('', '------------'),
          ('NOEMAIL', 'No Email will be sent.'),
          ('REMINDER', 'A Reminder mail will be sent to you 6 hours before event starts.'),
        )
    class Meta:
      model = Event
      exclude = excludes
      widgets = {
        'description': forms.CKEditorWidget(config={
            'toolbar': 'BasicWithImage',
            'width': 800,
            'height': 250,
            'forcePasteAsPlainText': 'true'
        },filemanager_url=filemanager_url)
      }
  return EventForm
