from django.contrib import admin

from internship.models import *

class InternshipPersonAdmin(admin.ModelAdmin):
  search_fields = ['student__user__username']
  def get_readonly_fields(self, request, obj=None):
    if obj: # obj is not None, so this is an edit
      return ['student',] # Return a list or tuple of readonly fields' names
    else: # This is an addition
      return []

admin.site.register(InternshipPerson, InternshipPersonAdmin)
admin.site.register(Company)
admin.site.register(CompanyApplicationMap)
admin.site.register(ForumPost)
admin.site.register(ForumReply)
admin.site.register(Results)
admin.site.register(Notices)
admin.site.register(Feedback)
