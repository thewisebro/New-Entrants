from django.contrib import admin
from messmenu.models import Menu

class MenuAdmin(admin.ModelAdmin):
  list_display = ('id', 
                  'bhawan', 
                  'date',
                  'time_of_day',
                  'content',
                  'sum_ratings',
                  'count_ratings',
                  'raters'
  )
  list_filter = ('date', 'bhawan')
  search_fields = ['bhawan']

admin.site.register(Menu, MenuAdmin)

