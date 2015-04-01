from nucleus.models import Batch , User , Course
from groups.models import Group , GroupInfo

group = Group.objects.get(nickname = 'IMG')
print group

