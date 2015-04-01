import os
from django import template
from softwares.constants import FILTERS
register = template.Library()

@register.filter
def hash(h,key):
    if key in h.keys():
        return h[key]
    else:
        return None

@register.filter
def image(h,key):
    if key in h.keys():
        return h[key].image
    else:
        return None

@register.filter
def div(value):
  if value>1073741824:
    return str(round(float(value)/1073741824,1))+" GB"
  else:
    return str(round(float(value)/1048576,1))+" MB"

@register.filter
def cutter(value):
  for x in FILTERS:
    value = value.replace(x,'')
  return value

@register.filter
def is_exists(self):
  return os.path.exists(self._get_path())
