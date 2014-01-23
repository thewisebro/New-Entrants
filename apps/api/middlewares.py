from django.http import Http404

from nucleus.models import User

class DelegateMiddleware(object):
  def process_view(self, request, view_func, view_args, view_kwargs):
    if request.user.is_authenticated():
      account_username = view_kwargs.pop('account_username', None)
      if account_username is None:
        request.owner = request.user.owner()
      else:
        account = User.objects.get_or_none(username=account_username)
        if account and request.user.accounts.filter(username=account.username).exists():
          request.owner = request.user.owner(account)
          request.user = request.owner.account
          request.account_username = account_username
        else:
          raise Http404
    return None
