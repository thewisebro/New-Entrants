from django.contrib import admin
from mcm.models import McmPerson, StudentLoanAid, MCM


class MCMAdmin(admin.ModelAdmin) :
  search_fields = [ 'student__user__username']
  exclude = ['person']

admin.site.register(McmPerson)
admin.site.register(StudentLoanAid)
admin.site.register(MCM, MCMAdmin)
