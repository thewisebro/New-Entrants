from django.contrib import admin
from helpcenter.models import *

class ReplyAdmin(admin.ModelAdmin):
  exclude = ('number',)

admin.site.register(Response)
admin.site.register(Reply,ReplyAdmin)
