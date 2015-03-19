from django.contrib.auth.models import User
from django.contrib.auth.models import Group as DjangoGroup
from groups.models import Group
from settings import PROJECT_ROOT

passwd_file = open(PROJECT_ROOT+'/nucleus/cc_passwd')
lines = list(passwd_file)

for line in lines:
  splits = line.split(':')
  username = splits[0]
  groupname = splits[3].replace('\n','')
  user = User.objects.get_or_create(username = username)[0]
  user.groups.add(DjangoGroup.objects.get(name='Student Group'))
  if not Group.objects.filter(user__username = username).exists():
    group = Group.objects.create(user = user,name = groupname,nickname = username.upper())
    print group
