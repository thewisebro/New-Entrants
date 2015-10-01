from django.contrib import admin
from gate.models import Gate


class GateAdmin(admin.ModelAdmin) :
  search_fields = [ 'prof__user__username']

admin.site.register(Gate, GateAdmin)
