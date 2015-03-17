from django.contrib import admin
from yaadein.models import *

from django.db.models import get_models, get_app

for model in get_models(get_app('yaadein')):
      admin.site.register(model)
