from django.contrib import admin

from placement.models import *

class PlacementPersonAdmin(admin.ModelAdmin):
  search_fields = ['student__user__username']
  def get_readonly_fields(self, request, obj=None):
    if obj: # obj is not None, so this is an edit
      return ['student',] # Return a list or tuple of readonly fields' names
    else: # This is an addition
      return []

admin.site.register(PlacementPerson, PlacementPersonAdmin)
admin.site.register(InternshipInformation)
admin.site.register(ProjectInformation)
admin.site.register(ExtraCurriculars)
admin.site.register(JobExperiences)
admin.site.register(LanguagesKnown)
admin.site.register(EducationalDetails)
admin.site.register(PlacementInformation)
admin.site.register(Company)
admin.site.register(CompanyApplicationMap)
admin.site.register(ForumPost)
admin.site.register(ForumReply)
admin.site.register(Feedback)
admin.site.register(Results)
admin.site.register(Notices)
admin.site.register(CPTMember)
admin.site.register(SecondRound)
admin.site.register(ContactPerson)
admin.site.register(CampusContact)
admin.site.register(CompanyContactInfo)
admin.site.register(CompanyContactComments)
