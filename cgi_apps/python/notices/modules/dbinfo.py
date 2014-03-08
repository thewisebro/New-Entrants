#!/usr/bin/python
"""
This module connects to db
"""

import _pg

def db_connect():
    try:
	db=_pg.connect(dbname="notices",host="192.168.121.9",user="board_gamers",passwd="b0ardg@mers")
	# notice_board   board_gamers   b0ardg@mers
	return db
    except:
	print "Error connecting to the database!"

"""
def intranet_db_connect():
    try:
 	db=_pg.connect(dbname="intranet",host="192.168.121.5",user="lectut",passwd="lectuT")
	return db
    except:
	print "Error connecting to the database!"
       
def regol_db_connect():
    try:
	rdb = _pg.connect(dbname="regolj",host="192.168.121.5",user="regolj",passwd="d0m!n0se!")
	return rdb
    except:
	print "Error connecting to the regol database!"
"""
