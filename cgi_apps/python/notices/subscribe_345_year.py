#!/usr/bin/python
"""This file makes all 3,4,5 th year students subscribed to Placement Office Notices.
"""
import sys
import os
current_app_path = os.getcwd()
#--->citing the path where user defined modules are stored
sys.path.append(current_app_path+"/modules")

import _pg
import dbinfo
import random
from include import *
import time
import binascii

db = dbinfo.db_connect()

def regol_db_connect():
    try:
	rdb = _pg.connect(dbname="regolj",host="192.168.121.5",user="regolj",passwd="d0m!n0se!")
	return rdb
    except:
	print "Error connecting to the regol database!"

regol_db = regol_db_connect()

def isvalidEmail(email):
    """
    """
    splits = email.split('@')
    if len(splits) == 2:
	if '.' in splits[1] :
	    return True
    return False	    

def toDb(username,email):
    """
    Inserts a user email id and prefernces to db
    """
    try:
        if not email:
	    return
	email = safeStrip(email)
        if not isvalidEmail(email):
            return "Invalid Email id"
        sent_to = "Placement:po"
        key=binascii.b2a_hex(username+str(time.gmtime()[5])+str(random.randint(1,1000)))
        db.query("delete from student_preference where userid = '"+username+"';") 
        db.query("INSERT into student_preference(userid,email_id,sent_to,key) values('"+username+"','"+email+"','"+sent_to+"','"+key+"');")
    except Exception ,e :
        print e

def add_345_year():
    result = regol_db.query("select person_id,alternate_email from person where course ='130' or course='140' or course='150';").dictresult()
    for row in result:
        if len(db.query("select * from student_preference where userid = '"+row['person_id']+"';").dictresult())==0:
	    print "Added",row['person_id'],row['alternate_email']
	    #toDb(row['person_id'],row['alternate_email'])

"""
def remove_alumni():
    result = db.query("select * from student_preference;").dictresult()
    for row in result:
        if len(regol_db.query("select person_id from person where person_id = '"+row['userid']+"';").dictresult())==0:
	    print "Removed",row['userid'],row['email_id']
	    db.query("delete from student_preference where userid = '"+row['userid']+"';")

def correct_db():
    result = db.query("select * from student_preference;").dictresult()
    for row in result:
        if len(row['key'].split('.'))==2:
	    userid =  row['userid']
            newkey=binascii.b2a_hex(userid+str(time.gmtime()[5])+str(random.randint(1,1000)))
	    db.query("update student_preference set key = '" + newkey + "' where userid='" + userid + "';")
	    print userid,row['key'],newkey
"""

if __name__ == '__main__':
  add_345_year()
