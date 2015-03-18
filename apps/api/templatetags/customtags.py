import json

from django.template import Library
from django.template.defaulttags import url as default_url
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape

from nucleus.constants import channeli_apps,external_links

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


@register.simple_tag(takes_context=True)
def pagelet_metadata(context, *args, **kwargs):
  django_messages = context.get('django_messages', [])
  escaped_messages = escape(str(django_messages))
  user = context.get('user')
  if user.is_authenticated():
    userdata = "<userdata username='%s' is_authenticated='true' />" % escape(
                user.username)
  else:
    userdata = "<userdata username='' is_authenticated='false' />"
  return mark_safe(userdata + ('<messages data="%s" />' % escaped_messages))

@register.filter
def jsonify(obj):
  return mark_safe(json.dumps(obj))

@register.simple_tag
def app_verbose_name(app):
  return channeli_apps[app]['name']

@register.simple_tag
def app_url(app):
  return channeli_apps[app]['url']

@register.simple_tag
def link_verbose_name(link):
  if link in external_links.keys():
    return external_links[link]['name']
  else:
    return channeli_apps[link]['name']

@register.simple_tag
def link_url(link):
  if link in external_links.keys():
    return external_links[link]['url']
  else:
    return channeli_apps[link]['url']
