from django.contrib import admin
from facapp.models import *


# class SearchBar(admin.ModelAdmin):
#   search_fields = ['title', 'professor']

admin.site.register(SectionPriority)
admin.site.register(Honors)
admin.site.register(ParticipationSeminar) # , SearchBar)
