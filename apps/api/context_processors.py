from django.utils.safestring import mark_safe

from nucleus.constants import channeli_apps, channeli_links,\
       login_page_links
from games.constants import channeli_games

def custom(request):
  context = {
    'channeli_apps': mark_safe(channeli_apps),
    'channeli_games': channeli_games,
    'channeli_links': channeli_links,
    'login_page_links':login_page_links,
  }
  context.update({
    'owner': request.owner if hasattr(request, 'owner') else None,
    'account_username': request.account_username \
        if hasattr(request, 'account_username') else None,
  })
  return context
