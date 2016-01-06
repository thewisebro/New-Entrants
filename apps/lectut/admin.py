from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin as ModelAdmin

# Register your models here.
from lectut.models import *

class PostAdmin(ModelAdmin):
  search_fields = ['course__code', 'upload_user__username']
  readonly_fields=('id',)

class UploadedfileAdmin(ModelAdmin):
  search_fields = ['post__id', 'upload_file']


admin.site.register(Reminders)
admin.site.register(Post , PostAdmin)
admin.site.register(Uploadedfile,UploadedfileAdmin)
