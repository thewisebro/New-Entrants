from nucleus.models import Batch , User , Course
from groups.models import Group , GroupInfo

group = Group.objects.get(nickname = 'IMG')
groupInfo = GroupInfo.objects.get(group = group)
members = groupInfo.members.all()

batches = Batch.objects.filter(id__in=[4550,4551,4552]).all()
for batch in batches:
  for member in members:
    try:
      batch.students.add(member)
      batch.save()
    except:
      pass

print 'success'
print group

