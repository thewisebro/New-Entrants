from django.contrib import admin

# Register your models here.
from lectut.models import LectutUser

class Userdetail(admin.ModelAdmin):
  fields = ['name']


admin.site.register(LectutUser , Userdetail)
