from django.contrib import admin

# Register your models here.

from facapp.models import *
# from nucleus.models import Faculty

class FacultyAdmin(admin.ModelAdmin):
  search_fields = ['faculty__name'] # ['user__username','name','employee_code']

# admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Honors)
admin.site.register(ParticipationSeminar)
admin.site.register(Membership)
admin.site.register(AdministrativeBackground)
admin.site.register(ProfessionalBackground)
admin.site.register(Miscellaneous)
admin.site.register(EducationalDetails)
admin.site.register(Collaboration)
admin.site.register(Invitations)
admin.site.register(MultiplePost)
admin.site.register(TeachingEngagement)
admin.site.register(Interests)
admin.site.register(SponsoredResearchProjects)
admin.site.register(ProjectAndThesisSupervision)
admin.site.register(PhdSupervised)
admin.site.register(ResearchScholarGroup)
admin.site.register(Visits)
admin.site.register(ParticipationInShorttermCourses)
admin.site.register(OrganisedConference)
admin.site.register(SpecialLecturesDelivered)
admin.site.register(FacSpace)