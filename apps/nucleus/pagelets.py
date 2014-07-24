from django.shortcuts import render

from nucleus.constants import tabs

def header(request):
  return render(request, 'nucleus/pagelets/header.html')

def sidebar(request):
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
  return render(request, 'nucleus/pagelets/sidebar.html', {'tabs': itabs})
