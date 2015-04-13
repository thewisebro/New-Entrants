import psycopg2
import MySQLdb

conn1 = psycopg2.connect("dbname='onatesha' user='bharat' host='localhost' password='test'")
cur1 = conn1.cursor()
cur1.execute("select * from notices")
rows = cur1.fetchall()

conn2 = MySQLdb.connect(host="localhost", user="channeli", passwd="channeli", db="fish")
cur2 = conn2.cursor()
for row in rows:
  cur2.execute("insert into notices_notice (datetime_modified, datetime_created, expire_date, contentdatetime_modified, ) values(%s, %s, %s)", )
