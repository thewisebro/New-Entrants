from django.contrib import admin
from facapp.models import Section


class SearchBar(admin.ModelAdmin):
  search_fields = ['title', 'professor']

admin.site.register(Section, SearchBar)
