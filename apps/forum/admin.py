from django.contrib import admin

from forum.models import *

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(Activity)
