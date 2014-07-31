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
  search_fields = ['username', 'name']

class BranchAdmin(ModelAdmin):
  search_fields = ['code', 'name', 'department']

class StudentAdmin(ModelAdmin):
  exclude = ['semester']
  search_fields = ['user__name', 'user__username']
  related_search_fields = {
    'user':('username',),
  }

class CourseAdmin(ModelAdmin):
  exclude = ['id']
  search_fields = ['code', 'name']

admin.site.register(User, UserAdmin)
admin.site.register(Owner)
admin.site.register(WebmailAccount)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentInfo)
admin.site.register(Course, CourseAdmin)
admin.site.register(RegisteredBranchCourse)
admin.site.register(RegisteredCourseChange)
admin.site.register(Batch)
admin.site.register(Faculty)
admin.site.register(GlobalVar)
admin.site.register(Alumni)
admin.site.register(StudentAlumni, StudentAdmin)
admin.site.register(StudentInfoAlumni)
admin.site.register(RegisteredCourseChangeAlumni)
