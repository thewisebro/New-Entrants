from django.contrib import admin
from bunkometer.models import Bunk,TimeTable,Course
# Register your models here.
admin.site.register(Bunk)
admin.site.register(TimeTable)
admin.site.register(Course)
