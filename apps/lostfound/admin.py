from django.contrib import admin
from lostfound.models import LostItems, FoundItems

admin.site.register(LostItems)
admin.site.register(FoundItems)
