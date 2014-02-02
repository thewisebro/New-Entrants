from django.utils.safestring import mark_safe

from nucleus.constants import channeli_apps

def custom(request):
  context = {
    'channeli_apps': mark_safe(channeli_apps),
  }
  context.update({
    'owner': request.owner if hasattr(request, 'owner') else None,
    'account_username': request.account_username \
        if hasattr(request, 'account_username') else None,
  })
  return context
