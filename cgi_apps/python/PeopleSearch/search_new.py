#! /usr/bin/python

import functions_new as functions
import db_queries_new as db_queries
import soundx

def simple_depriciated(search_string):
	"""Result of simpe search will be returned by this function.The formatted string must be passed as arguement."""
	#search_string=search_string.strip()
	#type=functions.get_content_type(search_string)
	#if type=="name" or type=="contact_num":
	#	result=simple_name(search_string)
	#elif type=="person_id":
	#	result=simple_person_id(search_string)
	result=simple_name(search_string.strip())
	return result


def simple(string):
	"""Handles the simple search if the entered field is a name.Requires the search string as arguement."""
	string = string.strip()
	result={}
	result['stud']=db_queries.student_name_query(string)
	result['fac'] =db_queries.faculty_name_query(string)
	result['serv']=db_queries.services_name_query(string)
	return result




def simple_person_id(string):
	"""Handles the simple search if the entered field is a telnet id.Requires the search string as arguement."""
	return db_queries.person_id_query(string)


def advanced(data):
	"""Handles advanced search and returns the result in the form of html table string"""
	#if functions.is_all_null(data)=="true":
	#	result=simple(data['srch']['str'])
	#	table=functions.toTables(result)
	#	return table
	if data['srch']['categ']=='stud':
		return functions.toStudTable(db_queries.adv_student(data['srch']['str'],data['stud']))
	if data['srch']['categ']=='fac':
		return functions.toFacTable(db_queries.adv_faculty(data['srch']['str'],data['fac']))
	if data['srch']['categ']=='serv':
		res=db_queries.adv_services(data['srch']['str'],data['serv'])
		if type(res)!="NoneType":
			return functions.toServTable(res)
		return {}
	return "An error occured while searching for your query.Please contact IMG.\nError code:SKE2"


