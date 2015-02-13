from buyandsell.models import *
#from channeli.models import *
from django.contrib import admin

class ItemsForSaleAdmin(admin.ModelAdmin):
  list_display = ('id','item_name','cost','status','user','category')
  search_fields = ['item__name']

class ItemsRequestedAdmin(admin.ModelAdmin):
  list_display = ('id','item_name','user','condition','price_upper','price_lower','category')
  search_fields = ['item_name']

class BuySellCategoryAdmin(admin.ModelAdmin):
  list_display=('main_category','name','code')
  search_fields=['name']  

#class PersonAdmin(admin.ModelAdmin):
# list_display=('person_id','name')
admin.site.register(SaleItems, ItemsForSaleAdmin)
admin.site.register(RequestedItems, ItemsRequestedAdmin)
admin.site.register(BuySellCategory,BuySellCategoryAdmin)  
