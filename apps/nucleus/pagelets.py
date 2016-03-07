from django.shortcuts import render

from nucleus.constants import tabs, DEFAULT_PASSWORD


def header_sidebar(request):
  if request.user.is_authenticated():
    group_names = request.user.groups.values_list('name', flat=True)
    itabs = filter(lambda t: t[2]==[] or (set(t[2]) & set(group_names)), tabs)
  else:
    itabs = filter(lambda t: not t[1], tabs)
  itabs = map(lambda t:{
    'name': t[0],
    'class': t[3],
    'color': t[4],
  }, itabs)
  context = {
    'tabs': itabs,
  }
  if request.user.is_authenticated():
    context.update({
      'pass_change': request.user.check_password(DEFAULT_PASSWORD),
      'not_viewed_notifications_count': request.user.usernotification_set\
        .filter(viewed=False).count(),
      'email_verified': request.user.useremail_set.filter(user=request.user, verified=True).count()!=0,
    })
  return render(request, 'nucleus/pagelets/header_sidebar.html', context)
