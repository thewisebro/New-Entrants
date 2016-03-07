from django.contrib import admin
from groups.models import Group,GroupInfo, GroupActivity
from django_extensions.admin import ForeignKeyAutocompleteAdmin as ModelAdmin

class GroupActivityAdmin(ModelAdmin):
  search_fields = ['text', 'group__nickname']
  list_display = ['group_nickname', 'text']
  def group_nickname(self, obj):
    return obj.group.nickname

admin.site.register(Group)
admin.site.register(GroupInfo)
admin.site.register(GroupActivity, GroupActivityAdmin)
