from django.contrib import admin
from notifications.models import *

admin.site.register(Notification)
admin.site.register(NotificationUser)
