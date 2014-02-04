from django.contrib import admin

from regol.models import *

class CourseAdmin(admin.ModelAdmin):
  search_fields = ['course_code']

admin.site.register(CourseDetails,CourseAdmin)
admin.site.register(CourseStructureMap)
admin.site.register(InstituteElectivesNotEligibleMap)
admin.site.register(RegolPerson)
admin.site.register(AssignedFaculty)
admin.site.register(PhdInfo)
admin.site.register(InstituteElectives)
admin.site.register(RegisteredCourses)
admin.site.register(JeeEntrants)
