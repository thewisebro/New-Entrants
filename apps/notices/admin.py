from django.contrib import admin
from notices.models import *

from core import forms

class NoticeAdmin(admin.ModelAdmin):
    formfield_overrides = {
          models.TextField: {'widget': forms.CKEditorWidget(config={'toolbar':'BasicWithImage'})},
    }
    search_fields = ['subject', 'uploader__user__username', 'uploader__user__name', 'uploader__category__name']

class NoticeUserAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__name']

admin.site.register(Notice, NoticeAdmin)
admin.site.register(TrashNotice)
admin.site.register(Category)
admin.site.register(NoticeUser, NoticeUserAdmin)
admin.site.register(Uploader)
