#! /usr/bin/python
import xlwt
import xlrd
import MySQLdb
import re

db = MySQLdb.connect("192.168.121.156","aniket","aniket","ci")

cursor=db.cursor()

workbook=xlrd.open_workbook('equipments.xls')
worksheet = workbook.sheet_by_name('Sheet1')

num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = -1
while curr_row < num_rows:
  curr_row += 1
  row = worksheet.row(curr_row)
  print 'Row:', curr_row
  curr_cell = -1
  c_val={}
  while curr_cell < num_cells:
      curr_cell += 1
      c_val[curr_cell] = worksheet.cell_value(curr_row, curr_cell)
      print c_val[curr_cell]
  # Prepare SQL query to INSERT a record into the database.
  sql = """INSERT INTO equip_entries(deptname,
           equipname, profname)
           VALUES (%s,%s,%s);"""
  try:
     c_val[2]=re.sub('   +','\n',c_val[2])
     # Execute the SQL command
     cursor.execute(sql,(c_val[0],c_val[1],c_val[2]))
     # Commit your changes in the database
     db.commit()
  except Exception as e:
     # Rollback in case there is any error
     db.rollback()
     print e


# disconnect from server
db.close()

