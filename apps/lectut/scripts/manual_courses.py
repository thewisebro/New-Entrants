''' This file manually creates some courses that were not available in the database 
    but present in lectut files. Run this script eveytime courses are added in
    the database '''

from nucleus.models import Course
course_list = ['HS-001BA','HS-001','CE-104WA','BT-204','CE-453','ICE-201','IHS-30','MT-332','EC-221','BT-202GE','ES-407HY','CE-202','IPH-102','EC-622','PEC-1','HS-001AB','IHY-101','EC-324','CH-001EN','IC-102','MA-207','IMA-17','CE-207','AS-103S','ES-201CI','CE-205','CE-206','MA-001QW','EC-102KR','CH-404','HSN-01','IIEQ-02','EC-431','VA-503','PH-102','EE-429','CS-252','HSN-01','PH-00S','DS-102']

success = 0
course_len = len(course_list)
for course in course_list:
  try:
    courseToAdd = Course(code = course, name = course, credits = 5, year = 2015)
    courseToAdd.save()
    success = success+1
  except Exception as e:
    print e

print 'Course-list'+str(course_len)
print 'Success : '+str(success)
