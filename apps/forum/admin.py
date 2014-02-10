from django.contrib import admin

from forum.models import *

class ProfileAdmin(admin.ModelAdmin):
  exclude = ('tags_followed',)

class QuestionAdmin(admin.ModelAdmin):
  exclude = ('tags',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Activity)
