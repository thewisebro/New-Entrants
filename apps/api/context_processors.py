from django.utils.safestring import mark_safe
from django.contrib import messages

from nucleus.constants import channeli_apps, channeli_links,\
       login_page_links
from games.constants import channeli_games

def custom(request):
  django_messages = []
  for message in messages.get_messages(request):
    django_messages.append({
      "level": message.level,
      "message": str(message.message),
      "extra_tags": str(message.tags),
    })

  context = {
    'channeli_apps': mark_safe(channeli_apps),
    'channeli_games': channeli_games,
    'channeli_links': channeli_links,
    'login_page_links': login_page_links,
    'django_messages': mark_safe(django_messages),
    'jb_user': getattr(request, 'jb_user', None),
  }
  context.update({
    'owner': request.owner if hasattr(request, 'owner') else None,
    'account_username': request.account_username \
        if hasattr(request, 'account_username') else None,
  })
  return context
