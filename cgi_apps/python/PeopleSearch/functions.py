#! /usr/bin/python
import types
import db_queries



def extract_person_id(string):
	"""extract person_id from the string entered in the "Search field".It will return 'telnetid' if the entered string is 'telnetid@iitr.ernet.in'."""
	return string.split('@')[0]


def is_person_id(string):
	"""Returns yes if it is a telnet id by checking the character at 8th position is '@' or not"""
	if len(string)<9:
		return "no"
	if string[8]=='@' :
		return "yes"
	return "no"



def get_content_type(string):
	"""Returns the type of search i.e. whether to search name,telnet id or contact number"""
	if is_person_id(string)=="yes" :
		return "person_id"
	else :
		return "name"

def assign_counts(query_result,splitted_name,id='person_id'):
	"""it assigns number of the matching search strings to each query row.Higher the count more accurate is the match.To be called like - result=assign_count(result,search_line)"""
	name = ' '.join(splitted_name)
#	zero=0
	for row in query_result:
		row['count']=0
		for part in splitted_name:
			if row[id] == part:
				row['count']+=10
			elif row[id].upper() == part.upper():
				row['count']+=5
			elif row[id].startswith(part):
				row['count']+=4
			elif row[id].upper().startswith(part.upper()):
				row['count']+=3
			elif len(part) >=3:
				if row[id].find(part) != -1:
					row['count']+=2
				elif row[id].upper().find(part.upper()) != -1:
					row['count']+=1
			if row['name'] == name:
				row['count']+=10
			elif row['name'].upper() == name.upper():
				row['count'] += 5
			elif row['name'].startswith(name):
				row['count'] += 4
			elif not row['name'].find(part)==-1 :
				row['count']+=1
			elif not row['name'].find(part.upper())==-1:	#to account for the entries in capital letters in db
				row['count']+=1
#		if row['count'] == 0:
#			zero=zero+1
#	print zero
	return query_result


def get_max_count(query):
	"""returns the maximum value of count(matches) in the query."""
	max=0
	for row in query:
		if row['count']>max:
			max=row['count']
	return max


def sort_query(query,search_string,id='person_id'):
	"""Sorts the query by count in descending order.It also removes duplicate rows from the query."""
	ret_query=[]    #Query to be returned
        query=assign_counts(query,split_the_name(search_string),id)
	max=get_max_count(query)
	zeroCount=20
        while max>=0:
                for row in query:
			if max == 0:
				if zeroCount == 0:
					return ret_query
				else:
					zeroCount-=1
                        if row['count']==max:
                                is_copied="no"
                                for copied in ret_query:        #check for duplicate rows in the query and if exists then do not copy the new row
                                        if copied[id]==row[id] :
                                                is_copied="yes"
                                if is_copied=="no" :
                                        ret_query.append(row)
                max-=1
	
        return ret_query



def split_the_name(name):
	"""it returns the name in well formatted manner"""
	name=name.lower()
        splitted_name=name.split(' ')
        strings=[]
        for part in splitted_name:
                strings.append(part.capitalize())
        return strings



def append_short_names(name):
	"""Appends short names to the dictionary of name in the end.The arguements are splitted parts of the query"""
	strings=name
	for part in name:		#to search for names like 'Mohan A.K.'     on search query like 'Ajay Mohan'
		if len(part)>1:
			strings.append(part.capitalize()[0]+'.')
	return strings


def is_all_null(form):
	"""returns whether all fields of selected tab are null or not"""
	tab=form['srch']['categ']
	if tab=='stud':
		if form[tab]['prog']=='null' and form[tab]['year']=='null' and form[tab]['dept']=='null':
			return "true"
		else:
			return "false"
	if tab=='fac':
		if form[tab]['dept']=='null' and form[tab]['post']=='null':
			return "true"
		else:
			return "false"
	if tab=='serv':
		if form[tab]['name']=='null':
			return "true"
		else:
			return "false"
	return "true"



def toStudTable(results):
	"""It takes the student db result as arguemeny.It return a string with html code of table with the result embeddded in it"""
	add_year_column(results)
	if len(results)!=0:
		string="\nSTUDENT RESULTS<br><table cellspacing='0' class='table_result'>\n\t<tr class='table_head'>\n\t\t<td>USER ID</td>\n\t\t<td>NAME</td>\n\t\t<td>DISCIPLINE</td>\n\t<td>DEGREE</td><td>YEAR</td></tr>\n"
		for row in results:
			string=string+"\t<tr>\n\t\t<td>"+row['person_id']+"</td>\n\t\t<td><a href='http://people.iitr.ernet.in/shp/"+row['enrollment_no']+"' target='_blank'>"+row['name'].upper()+"</a></td>\n\t\t<td>"+row['deptt']+"</td>\n\t<td>"
			if type(row['degree']) is not types.NoneType:
				string+=row['degree']
			string+="</td><td>"+str(row['year'])+"</td></tr>\n"
		string=string+"</table>"
		return string
	return ""


def toFacTable(results):
	"""It takes the student db result as argument.Returns a string with html code of table with the result embedded in it"""
	if len(results)==0:
		return ""
	string="\nFACULTY RESULTS<br /><table cellspacing='0' class='table_result'>\n\t<tr class='table_head'>\n\t\t<td>USER ID</td>\n\t\t<td>NAME</td>\n\t\t<td>DEPARTMENT</td>\n\t\t<td>DESIGNATION</td>\n\t</tr>\n"
	for row in results:
		string=string+"\t<tr>\n\t\t<td>"+row['faculty_id']+"</td>\n\t\t<td><a href='"+db_queries.get_fac_url(row['faculty_id'])+"' target='_blank'>"+row['name'].upper()+"</a></td>\n\t\t<td>"+row['deptt']+"\n\t\t<td>"+row['post_name']+"</td>\n\t</tr>\n"
	string=string+"</table>"
	return string



def toServTable(results):
	"""Function to convert result dictionary of services to table string in html code"""
	if len(results)==0:
		return ""
	string="\nSERVICE RESULTS<br>\n<table cellspacing='0' class='table_result'>\n\t<tr class='table_head'>\n\t\t<td>NAME</td>\n\t\t<td>OFFICE NUMBER</td>\n\t\t<td>\n\t\tSERVICE</td>\n\t</tr>\n"
	for row in results:
		string=string+"\t<tr>\n\t\t<td>"+row['name'].upper()+"</td>\n\t\t<td>"+row['office']+"</td>\n\t\t<td>\n\t\t"+row['type']+"</td?\n\t</tr>\n"
	string=string+"</table>"
	return string



def toTables(data):
	"""Intakes the double dictionary of simple search result and returns the string with html code for tables for student,faculty and services search results"""
	table=""
	if len(data['stud']) !=0:
		table=table+toStudTable(data['stud'])
	if len(data['fac']) !=0:
		table=table+toFacTable(data['fac'])
	if len(data['serv']) !=0:
		table=table+toServTable(data['serv'])
	return table



def to_dept_dict(list):
	"""It takes the list of departments and returns the dictionary.The keys are the department codes and values are their names."""
	dict={}
	for row in list:
		dict[row['department_code']]=row['department_name']
	return dict


#def strip_name(name):
#	"""It checks for special characters in the string and returns the string containing only alphabets,numbers and spaces"""


def remove_special_characters(string,characters="\'\"\\/=-<>!+"):
	"""Removes special characters from the passed string.It can also take a second string made of special characters(escaped from python)."""
	for char in characters:
		string=string.replace(char,'')
	return string



"""
ug
pg
phd


year(0 and 1) or 1st and 2nd sem


221


321

"""

def add_year_column(list):
	"""It takes list list of student query results and add a column named year according to their course."""
	i=len(list)-1
	while i>=0:
		course=list[i]['course']/100
		if course is 1:
			list[i]['year']=(list[i]['course']%100)/10;
		else:
			list[i]['year']=((list[i]['course']%100)-19)/2;
		i-=1
