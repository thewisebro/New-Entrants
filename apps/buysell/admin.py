from buysell.models import *
#from channeli.models import *
from django.contrib import admin

class ItemsForSaleAdmin(admin.ModelAdmin):
  list_display = ('id','item_name','cost','status','user')
  search_fields = ['item__name']

class ItemsRequestedAdmin(admin.ModelAdmin):
  list_display = ('id','item_name','user','condition')
  search_fields = ['item_name']


#class PersonAdmin(admin.ModelAdmin):
# list_display=('person_id','name')
admin.site.register(ItemsForSale, ItemsForSaleAdmin)
admin.site.register(ItemsRequested, ItemsRequestedAdmin)
