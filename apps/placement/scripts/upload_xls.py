import xlrd
def ExcelParser(sheet_name):
  import ipdb; ipdb.set_trace()
  workbook = xlrd.open_workbook(sheet_name)
  worksheet = workbook.sheet_by_name("Sheet1")
  num_rows = worksheet.nrows - 1
  curr_row = 0
  rows = []
  while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)
    row = {'roll':row[0].value , 'cgpa':row[2].value , 'sgpa':row[9].value}
    rows.append(row)
  return rows
