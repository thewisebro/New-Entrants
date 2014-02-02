import json

from django.template import Library
from django.template.defaulttags import url as default_url
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = Library()

@register.tag
def url(parser, token):
  urlnode = default_url(parser, token)
  actual_render = urlnode.render
  def custom_render(context):
    account_username = context.get('account_username', None)
    if account_username:
      return '/u/' + account_username + actual_render(context)
    else:
      return actual_render(context)
  urlnode.render = custom_render
  return urlnode

@register.simple_tag(takes_context=True)
def pagelet(context, pagelet_name, *args, **kwargs):
  account_username = context.get('account_username', None)
  url = ''
  if account_username:
    url = '/u/' + account_username + reverse(pagelet_name, args=args, kwargs=kwargs)
  else:
    url = reverse(pagelet_name, args=args, kwargs=kwargs)
  return """<div id="%s" class="pagelet" pagelet-url="%s"></div>""" % (pagelet_name, url)


@register.filter
def jsonify(obj):
  return mark_safe(json.dumps(obj))
