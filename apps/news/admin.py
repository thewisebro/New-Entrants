from django.contrib import admin
from news.models import *

"""
class ChannelPrefAdmin(admin.ModelAdmin):
  exclude = ('pref_order',)
"""

admin.site.register(NewsUser)
admin.site.register(News)
admin.site.register(Channel)
admin.site.register(Source)
admin.site.register(ChannelPref)
admin.site.register(SourcePref)

