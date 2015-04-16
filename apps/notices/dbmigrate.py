from notices.models import *
from notices.constants import *

import psycopg2
import MySQLdb
import datetime


conn1 = psycopg2.connect("dbname='onatesha' user='board_gamers' host='192.168.121.9' password='b0ardg@mers'")
cur1 = conn1.cursor()
print "connected to psql database.."
cur1.execute("select * from notices")
rows = cur1.fetchall()
print "rows fetched from psql.."

conn2 = MySQLdb.connect(host="192.168.121.9", user="channeli", passwd="!ns@nity", db="newchanneli")
cur2 = conn2.cursor()
print "connected to mysql database."
u=User.objects.get(username="admin")
f = open('apps/notices/log.txt', 'r+')
count=0
for row in rows:
  cat=row[6]
  if row[6]=='Dean':
	cat='Deans'
  if count==0:
  	print cat
  c=Category.objects.get(name=cat)
  uploader = Uploader.objects.get(user=u, category=c)
  f1 = open("apps/notices/data/n" + str(row[0]), 'r')
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

cur1.execute("select * from old_notices")
rows = cur1.fetchall()

count=0
for row in rows:
  cat=row[6]
  if row[6]=='Dean':
	cat='Deans'
  elif row[6]=='Dr. Aalok Misra':
	cat='Physics'
  elif row[6]=='IMG':
	cat='Admin'
  elif row[6]=='ADAP':
	continue
  elif row[6]=='Paper Tech. Dept.':
	continue
  elif row[6]=='JEE Office':
	continue
  try:
	  c=Category.objects.get(name=cat)
  except:
	print "category "+cat	
  uploader = Uploader.objects.get(user=u, category=c)
  try:
	  f1 = open("apps/notices/data/n" + str(row[0]), 'r')
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
