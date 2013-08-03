from django.contrib import admin

from nucleus.models import *

class BranchAdmin(admin.ModelAdmin):
  search_fields = ['code', 'name', 'department']

class CUserAdmin(admin.ModelAdmin):
  search_fields = ['name', 'username']

class StudentAdmin(admin.ModelAdmin):
  search_fields = ['name', 'username']
  exclude = ['groups']

admin.site.register(CUser, CUserAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentInfo)
