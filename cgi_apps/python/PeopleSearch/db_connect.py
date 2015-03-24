#! /usr/bin/python
import _pg

def connect_to_people_search() :
	"""Connects to the test database"""
	try :
		db=_pg.connect(dbname="people_search",host="192.168.121.9",user="people_search",passwd="se@rch!t")
		return db
	except :
		print "Can not connect to the test database"

def connect_to_test() :
	"""Connects to the test database"""
	try :
		db=_pg.connect(dbname="test",host="192.168.121.5",user="test",passwd="test")
		return db
	except :
		print "Can not connect to the test database"


def connect_to_regolj() :
	"""Connects to the regolj database"""
	try:
		db=_pg.connect(dbname="regolj",host="192.168.121.5",user="regolj",passwd="d0m!n0se!")
		return db
	except :
		print "Can not connect to the regolj database"


def connect_to_facapp():
	"""Returns the db odjact connected to facapp"""
	try:
		db=_pg.connect(dbname="facappn",host="192.168.121.5",user="facapp",passwd="Term!n@t0r@pp")
		return db
	except:
		print "Cannot connect to the faculty db."

def connect_to_cms():
	"""Returns the db object connected to CMS"""
	try:
		db=_pg.connect(dbname="cms",host="192.168.121.5",user="cms",passwd="cms")
		return db
	except:
		print "Cannot connect to the cms database."
