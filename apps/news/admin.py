from django.contrib import admin
from news.models import *

"""
class ChannelPrefAdmin(admin.ModelAdmin):
  exclude = ('pref_order',)
"""
class NewsAdmin(admin.ModelAdmin):
  search_fields = ['title', 'source__name', 'channel__name']

admin.site.register(NewsUser)
admin.site.register(News, NewsAdmin)
admin.site.register(Channel)
admin.site.register(Source)
admin.site.register(ChannelPref)
admin.site.register(SourcePref)

