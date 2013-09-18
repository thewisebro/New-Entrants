def custom(request):
  context = {}
  context.update({
    'owner': request.owner if hasattr(request, 'owner') else None,
    'account_username': request.account_username \
        if hasattr(request, 'account_username') else None,
  })
  return context
