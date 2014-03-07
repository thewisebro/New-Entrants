from django.contrib import admin

from games.models import *

class GameScoreAdmin (admin.ModelAdmin):
  list_display = ['student', 'gamecode', 'score']
  search_fields = ['student__user__name', 'gamecode', 'score']

class GameSessionAdmin (admin.ModelAdmin):
  list_display = ['student', 'gamecode', 'start_time']
  search_fields = ['student__user__name', 'gamecode']

admin.site.register(GameScore, GameScoreAdmin)
admin.site.register(GameSession, GameSessionAdmin)
