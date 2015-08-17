from nucleus.models import *
import json

new_semester = {
  'UG10':'UG11',
  'UG11':'UG20',
  'UG20':'UG21',
  'UG21':'UG30',
  'UG30':'UG31',
  'UG31':'UG40',
  'UG40':'UG41',
  'UG41':'UG50',
  'UG50':'UG51',
  'UG51':'UG0',
  'PG10':'PG11',
  'PG11':'PG20',
  'PG20':'PG21',
  'PG21':'PG30',
  'PG30':'PG31',
  'PG31':'PG0',
  'PHD10':'PHD11',
  'PHD11':'PHD20',
  'PHD20':'PHD21',
  'PHD21':'PHD30',
  'PHD30':'PHD31',
  'PHD31':'PHD40',
  'PHD40':'PHD41',
  'PHD41':'PHD50',
  'PHD50':'PHD51',
  'PHD51':'PHD60',
  'PHD60':'PHD61',
  'PHD61':'PHD70',
  'PHD70':'PHD71',
  'PHD71':'PHD80',
  'PHD80':'PHD81',
  'PHD81':'PHD90',
  'PHD90':'PHD91',
  'PHD91':'PHD0',
}

students = Student.objects.filter(passout_year=None).exclude(semester__in=['UG0','PG0','ST1','ST2','ST3','ST4','DPLM','10TH','12TH','PHD0','UG00'])
print 'Students :',len(students)
bugs = []
misc_bugs = []
misc_bug = 0
bug = 0
done = 0

for (i,stud) in enumerate(students):
	try:
		stud.semester_no += 1
		stud.save()
		done+=1
	except KeyError:
		print i, stud.user.username
		break
	except:
		misc_bugs.append(stud.user.username)
		misc_bug+=1

print 'done: ',done
print 'bugs: ',bug
print 'misc_bugs: ',misc_bugs

bugs_js = open('bugs.json','w+')
misc_js = open('misc.json','w+')

json.dump(bug,bugs_js)
json.dump(misc_bugs,misc_js)

print 'Phewww.....'
"""
done=0
bugs=[]
bug=0

students = Person.objects.filter(passout_year=None)

print 'Passing out ...', len(students)

for (i,stud) in enumerate(students):
	try:
		if 
		adm_year=int(stud.admission_year)
		duration=stud.branch.duration
		stud.passout_year=duration+adm_year
		stud.save()
		done+=1
	except:
		bugs.append(stud.user.username)
		bug+=1

print 'done: ',done
print 'bug: ',bug

passout_bugs = open('passout_bugs.json','w+')
json.dump(bugs,passout_bugs)"""
