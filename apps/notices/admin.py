from django.contrib import admin
from notices.models import *

from core import forms

class NoticeAdmin(admin.ModelAdmin):
    formfield_overrides = {
          models.TextField: {'widget': forms.CKEditorWidget(config={'toolbar':'BasicWithImage'})},
    }
    search_fields = ['subject', 'uploader__user','uploader__user__username']

admin.site.register(Notice, NoticeAdmin)
admin.site.register(TrashNotice)
admin.site.register(Category)
admin.site.register(NoticeUser)
admin.site.register(Uploader)
