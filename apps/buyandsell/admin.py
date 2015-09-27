from buyandsell.models import *
#from channeli.models import *
from django.contrib import admin

class ItemsForSaleAdmin(admin.ModelAdmin):
  list_display = ('id','item_name','cost','user','category')
  search_fields = ['item__name']

class ItemsRequestedAdmin(admin.ModelAdmin):
  list_display = ('id','item_name','user','price_upper','category')
  search_fields = ['item_name']

class BuySellCategoryAdmin(admin.ModelAdmin):
  list_display=('main_category','name','code')
  search_fields=['name']

class SuccessfulTransactionAdmin(admin.ModelAdmin):
  list_display=('seller','buyer','sell_item','request_item','is_requested','trasaction_date','feedback')


#class PersonAdmin(admin.ModelAdmin):
# list_display=('person_id','name')
admin.site.register(SaleItems, ItemsForSaleAdmin)
admin.site.register(RequestedItems, ItemsRequestedAdmin)
admin.site.register(BuySellCategory,BuySellCategoryAdmin)
admin.site.register(SuccessfulTransaction,SuccessfulTransactionAdmin)
