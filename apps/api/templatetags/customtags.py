from django.template import Library
from django.template.defaulttags import url as default_url

register = Library()

@register.tag
def url(parser, token):
  urlnode = default_url(parser, token)
  actual_render = urlnode.render
  def custom_render(context):
    account_username = context['account_username']
    if account_username:
      return '/u/' + account_username + actual_render(context)
    else:
      return actual_render(context)
  urlnode.render = custom_render
  return urlnode
