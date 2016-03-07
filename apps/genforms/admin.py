from django.contrib import admin
from genforms.models import *

class LibFormAdmin(admin.ModelAdmin):
    list_display = ('person','valid_till')
    search_fields = ['person__user__username', 'person__name']

admin.site.register(LibForm, LibFormAdmin)
