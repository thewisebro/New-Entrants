from django import template
register = template.Library()

@register.filter
def enter(value):
  return value.replace('\n','<br>')
