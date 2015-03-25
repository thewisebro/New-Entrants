#! /usr/bin/python
import search
import functions
import db_queries

len_min = 4

def printresult(data):
	"""Searches for the formatted string.The formatted string is passed as the arguement."""
	result={}
	result=db_queries.exact_id_query(data['srch']['str'])
	if len(result['stud'])==1 or len(result['fac'])==1:
		table=functions.toTables(result)
	elif data['srch']['categ'] == 'all' :
		if len(data['srch']['str']) < len_min :
			table = ""
		else :
			result=search.simple(data['srch']['str'])
			table=functions.toTables(result)
	elif data['srch']['adv'] == "off":
		if len(data['srch']['str']) < len_min :
			table = ""
		elif data['srch']['categ'] == 'stud':
			result['stud'] = db_queries.student_name_query(data['srch']['str'])
			result['stud'] = functions.sort_query(result['stud'],data['srch']['str'])
			table = functions.toStudTable(result['stud'])
		elif data['srch']['categ'] == 'fac':
			result['fac'] = db_queries.faculty_name_query(data['srch']['str'])
			result['fac'] = functions.sort_query(result['fac'],data['srch']['str'],"faculty_id")
			table = functions.toFacTable(result['fac'])
		else:
			result['serv'] = db_queries.services_name_query(data['srch']['str'])
#			result['serv'] = functions.sort_query(result['serv'],data['srch']['str'])
			table = functions.toServTable(result['serv'])
	else:
		table = search.advanced(data)
	if len(table)==0:
		print "No results for your query"
	else:
		print table
		
