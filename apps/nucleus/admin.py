from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django_extensions.admin import ForeignKeyAutocompleteAdmin as ModelAdmin
from core import forms
from nucleus.models import *

def getUserCreationForm(usermodel):
  class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
      model = usermodel
      fields = ("username",)

    def clean_password2(self):
      # Check that the two password entries match
      password1 = self.cleaned_data.get("password1")
      password2 = self.cleaned_data.get("password2")
      if password1 and password2 and password1 != password2:
        raise forms.ValidationError("Passwords don't match")
      return password2

    def save(self, commit=True):
      # Save the provided password in hashed format
      user = super(UserCreationForm, self).save(commit=False)
      user.set_password(self.cleaned_data["password1"])
      if commit:
        user.save()
      return user
  return UserCreationForm

def getUserChangeForm(usermodel):
  class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label="Password",
      help_text="Raw passwords are not stored, so there is no way to see "
                "this user's password, but you can change the password "
                "using <a href=\"password/\">this form</a>.")

    class Meta:
      model = usermodel
      fields = '__all__'

    def clean_password(self):
      # Regardless of what the user provides, return the initial value.
      # This is done here, rather than on the field, because the
      # field does not have access to the initial value
      return self.initial["password"]
  return UserChangeForm

class UserAdmin(AuthUserAdmin):
  form = getUserChangeForm(User)
  add_form = getUserCreationForm(User)
  fieldsets = (
      (None, {'fields': ('username', 'password')}),
      ('Personal info', {'fields': ('first_name', 'last_name', 'email',
                                    'name', 'photo', 'gender', 'birth_date',
                                    'contact_no')}),
      ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                     'groups', 'user_permissions')}),
      ('Important dates', {'fields': ('last_login', 'date_joined')}),
  )
  ordering = ('username',)
  filter_horizontal = ('groups', 'user_permissions',)
  search_fields = ['username', 'name', 'email']

class WebmailAdmin(ModelAdmin):
  search_fields = ['webmail_id', 'user__username','user__name']
  list_display = ['webmail_id', 'user']

class BranchAdmin(ModelAdmin):
  search_fields = ['code', 'name', 'department']

class StudentAdmin(ModelAdmin):
  exclude = ['semester']
  search_fields = ['user__name', 'user__username']
  related_search_fields = {
    'user':('username',),
  }
  list_display = ['student_enr_no', 'student_name', 'branch', 'student_year']
  list_filter = ['branch__degree', 'branch__department', 'branch__graduation', 'semester_no']
  def student_enr_no(self, obj):
    return obj.user.username
  def student_name(self, obj):
    return obj.user.name
  def student_year(self, obj):
    return (obj.semester_no + 1)/2
  student_enr_no.short_description = 'Enrollment Number'
  student_name.short_description = 'Name'
  student_year.short_description = 'Year'

class StudentUserAdmin(ModelAdmin):
  search_fields = ['name', 'username']
  def has_add_permission(self, request):
    return False

class CourseAdmin(ModelAdmin):
  exclude = ['id']
  search_fields = ['code', 'name']

class FacultyAdmin(ModelAdmin):
  search_fields = ['user__username', 'user__name']
  list_display = ['user', 'department', 'designation']
  list_filter = ['department','designation']

admin.site.register(User, UserAdmin)
admin.site.register(Owner)
admin.site.register(WebmailAccount, WebmailAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentInfo)
admin.site.register(StudentUser, StudentUserAdmin)
admin.site.register(StudentUserInfo, StudentUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(RegisteredCourse)
admin.site.register(Batch)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(GlobalVar)
admin.site.register(Alumni)
