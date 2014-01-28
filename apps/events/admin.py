from django.contrib import admin

from events.models import *
from core import forms

class EventAdmin(admin.ModelAdmin):
  formfield_overrides = {
    models.TextField: {'widget': forms.CKEditorWidget(config={'toolbar':'BasicWithImage'})},
  }

admin.site.register(Calendar)
admin.site.register(Event, EventAdmin)
admin.site.register(EventsUser)
