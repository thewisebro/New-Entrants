#from notices.models import *

import psycopg2
import MySQLdb
import datetime

for c in Category.objects.all():
    up = Uploader(user=u, name=u.username+"_"+c.main_category+"_" +c.name.replace(" ", "_"), category=c)
    up.save()

conn1 = psycopg2.connect("dbname='onatesha1' user='postgres' host='localhost' password='computer'")
cur1 = conn1.cursor()
print "connected to psql database.."
cur1.execute("update notices set sent_from='Deans' where sent_from='Dean'")
cur1.execute("select * from notices")
rows = cur1.fetchall()

conn2 = MySQLdb.connect(host="localhost", user="root", passwd="computer", db="channeli")
cur2 = conn2.cursor()
print "connected to mysql database."
u=User.objects.get(username="admin")
f = open('log.txt', 'r+')
count=0
for row in rows:
  c=Category.objects.get(name=row[6])
  uploader = Uploader.objects.get(user=u, category=c)
  f1 = open("data/n" + str(row[0]), 'r')
  html = f1.read()
  ref=row[5]
  emailsend=row[9]
  re_edited=row[10]
  if(row[5]=="null"):
	ref=0
  if(row[9]=="yes"):
	emailsend="true"
  if(row[9]=="no"):
	emailsend="false"

  if(row[10]=="yes"):
	re_edited="true"
  if(row[10]=="no"):
	re_edited="false"
  dm = datetime.datetime.strptime(row[1], '%d-%m-%Y %I:%M %p').strftime('%Y-%m-%d %H:%M:%S')
  dc = datetime.datetime.strptime(row[2], '%d-%m-%Y %I:%M %p').strftime('%Y-%m-%d %H:%M:%S')
  ed = datetime.datetime.strptime(row[3], '%d-%m-%Y').date().strftime('%Y-%m-%d %H:%M:%S')

  try:
	  cur2.execute("insert into notices_notice (content, datetime_modified, datetime_created, expire_date, subject, reference, uploader_id, emailsend, re_edited, expired_status) values(\"%s\", \"%s\", \"%s\", \"%s\", \"%s\",\"%s\", %s, %s, %s, %s)" % (conn2.escape_string(html), dm, dc, ed, row[4], ref, uploader.id, emailsend, re_edited, "false"))
  except:
		print row[4]	
		f.write(row[4])
		f.write("\n")
  count = count+1
  print str(count) + "/" + str(len(rows))
  f.write(str(count) + "/" + str(len(rows)))
  f.write("\n")
print "new notices done\n"
f.write("new notices done\n")

cur1.execute("update old_notices set sent_from='Physics' where sent_from='Dr. Aalok Misra';")
cur1.execute("update old_notices set sent_from='Deans' where sent_from='Dean'")
cur1.execute("select * from old_notices")
cur1.execute("delete from old_notices where sent_from='ADAP'")
cur1.execute("delete from old_notices where sent_from='Paper Tech. Dept.'")
cur1.execute("delete from old_notices where sent_from='JEE Office'")
cur1.execute("update old_notices set sent_from='Admin' where sent_from='IMG'")
cur1.execute("select * from old_notices")
rows = cur1.fetchall()

count=0
for row in rows:
  c=Category.objects.get(name=row[6])
  uploader = Uploader.objects.get(user=u, category=c)
  try:
	  f1 = open("data/n" + str(row[0]), 'r')
	  html = f1.read()
  except:
	print "file not opening " + str(row[0])
	continue
  ref=row[5]
  emailsend=row[9]
  re_edited=row[10]
  if(row[5]=="null"):
	ref=0
  if(row[9]=="yes"):
	emailsend="true"
  if(row[9]=="no"):
	emailsend="false"

  if(row[10]=="yes"):
	re_edited="true"
  if(row[10]=="no"):
	re_edited="false"
  try:
	  dm = datetime.datetime.strptime(row[1], '%d-%m-%Y %I:%M %p').strftime('%Y-%m-%d %H:%M:%S')
	  dc = datetime.datetime.strptime(row[2], '%d-%m-%Y %I:%M %p').strftime('%Y-%m-%d %H:%M:%S')
  except:
	  dm = datetime.datetime.strptime(row[1], '%d-%m-%Y').strftime('%Y-%m-%d %H:%M:%S')
	  dc = datetime.datetime.strptime(row[2], '%d-%m-%Y').strftime('%Y-%m-%d %H:%M:%S')
  try:
  	ed = datetime.datetime.strptime(row[3], '%d-%m-%Y').date().strftime('%Y-%m-%d %H:%M:%S')
  except:
	print row[4]	
	f.write(row[4])
	f.write("\n")

  try:
	  cur2.execute("insert into notices_notice (content, datetime_modified, datetime_created, expire_date, subject, reference, uploader_id, emailsend, re_edited, expired_status) values(\"%s\",\"%s\", \"%s\", \"%s\", \"%s\",\"%s\", %s, %s, %s, %s)" % (conn2.escape_string(html),dm, dc, ed, row[4], ref, uploader.id, emailsend, re_edited, "true"))
  except:
	print row[4]	
	f.write(row[4])
	f.write("\n")
  count = count+1
  print str(row[0]) + " " + str(count) + "/" + str(len(rows))
  f.write(str(row[0]) + " " + str(count) + "/" + str(len(rows)))
  f.write("\n")
print "new notices done\n"
f.write("new notices done\n")

conn1.commit()
conn2.commit()
