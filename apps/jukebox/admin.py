from django.contrib import admin
from jukebox.models import *
from django_extensions.admin import ForeignKeyAutocompleteAdmin as ModelAdmin

class AlbumAdmin(ModelAdmin):
  search_fields = ['id', 'album']

class ArtistAdmin(ModelAdmin):
  search_fields = ['id', 'artist']

class SongAdmin(ModelAdmin):
  search_fields = ['id', 'song']

class PlaylistAdmin(ModelAdmin):
  search_fields = ['id', 'name', 'person__person__username']

admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Genre)
admin.site.register(Playlist, PlaylistAdmin)
