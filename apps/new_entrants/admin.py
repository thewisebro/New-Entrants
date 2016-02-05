from django.contrib import admin
from new_entrants.models import *
from nucleus.models import Student

class StudentProfileAdmin(admin.ModelAdmin):
  list_display = ('user','get_name','email','fb_link','state','hometown','phone_no','phone_privacy','profile_privacy')
  search_fields = ['user__name']

  def get_readonly_fields(self, request, obj=None):
    return self.readonly_fields + ('email', 'hometown', 'state', 'phone_no', 'user')

  def get_name(self,obj):
    return obj.user.name

class SeniorProfileAdmin(admin.ModelAdmin):
  list_display = ('user','get_name','email','fb_link','state','hometown','phone_no')
  search_fields = ['user__name']

  def get_readonly_fields(self, request, obj=None):
    return self.readonly_fields + ('email', 'hometown', 'state', 'phone_no', 'user')

  def get_name(self,obj):
    return obj.user.name

class BlogsAdmin(admin.ModelAdmin):
  list_display = ('title','date_published','get_group','description')
  search_fields = ['title']
  exclude = ('content',)

  def get_group(self,obj):
    return obj.group.user.username

  def has_add_permission(self, request):
    return False

  def get_readonly_fields(self, request, obj=None):
    return self.readonly_fields + ('title','description','group','date_published')

class RequestsAdmin(admin.ModelAdmin):
  list_display = ('get_studentName','get_seniorName','is_accepted')
  search_fields = ['student_profile__user__name','senior_profile__user__name']

  def get_studentName(self,obj):
    return obj.student_profile.user.name

  def get_seniorName(self,obj):
    return obj.senior_profile.user.name


# Register your models here.
admin.site.register(Student_profile, StudentProfileAdmin)
admin.site.register(Senior_profile, SeniorProfileAdmin)
admin.site.register(Blog, BlogsAdmin)
admin.site.register(Request, RequestsAdmin)
