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
    row = {'roll':row[0].value ,'sem_no':row[5].value, 'cgpa':row[6].value , 'sgpa':row[7].value}
    rows.append(row)
  return rows
