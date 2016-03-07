import xlrd
def ExcelParser(workbook_name, sheet_name):
  workbook = xlrd.open_workbook(workbook_name)
  worksheet = workbook.sheet_by_name(sheet_name)
  num_rows = worksheet.nrows - 1
  curr_row = 0
  rows = []
  while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)
    row = {'roll':row[0].value ,'sem_no':row[3].value, 'cgpa':row[5].value , 'sgpa':row[4].value}
    rows.append(row)
  return rows
