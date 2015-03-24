#! /usr/bin/python
import _pg
import soundx
import db_connect

def update_fac_table():
	db=db_connect.connect_to_facapp()
	result=db.query("select name,faculty_id from general_information")
	results=[]
	results.extend(result.dictresult())
	for row in results:
		name_parts=row['name'].split(" ")
		soundex=""
		for part in name_parts:
			if not part == "":
				soundex+=soundx.soundxfunction(part,"true")+" "
		print "name:",row['name'],",soundex:",soundex,"   id:"+row['faculty_id']
		db.query("update fac_soundx set soundx='"+soundex+"' where faculty_id ='"+row['faculty_id']+"'")



def update_stud_table():
	db=db_connect.connect_to_regolj()
	db.query("delete from person_soundx")
	result=db.query("select name,person_id from person_extended")
	results=[]
	results.extend(result.dictresult())
	for row in results:
		name_parts=row['name'].split(" ")
		soundex=""
		for part in name_parts:
			if not part == "":
				soundex+=soundx.soundxfunction(part,"true")+" "
		print "name:",row['name'],",soundex:",soundex,"   id:"+row['person_id']
		#db.query("update person_soundx set soundx='"+soundex+"' where person_id='"+row['person_id']+"'")
		db.query("insert into person_soundx (person_id,soundx) values ('"+row['person_id']+"','"+soundex+"')")
#update_fac_table()
update_stud_table()
