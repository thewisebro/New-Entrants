import json
from pprint import pprint
from nucleus.models import Course

with open('apps/lectut/scripts/batch.json') as json_data:
  values = json.load(json_data)
  json_data.close()
#  pprint(values)

  for batch in values:
#    print batch
    code = batch['course_code']
    if Course.objects.filter(code = code).exists():
      print Course.objects.get(code = code)
