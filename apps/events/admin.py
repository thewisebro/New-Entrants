from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin as ModelAdmin

from events.models import *
from core import forms

class EventAdmin(admin.ModelAdmin):
  formfield_overrides = {
    models.TextField: {'widget': forms.CKEditorWidget(config={'toolbar':'BasicWithImage'})},
  }

class EventsUserAdmin(ModelAdmin):
  search_fields = ['user__username']

class CalendarAdmin(admin.ModelAdmin):
  search_fields = ['name']

admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventsUser, EventsUserAdmin)
