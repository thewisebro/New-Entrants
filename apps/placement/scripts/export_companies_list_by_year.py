import xlwt
from placement.models import Company

def export_company_data_to_excel( year ):
  cs = Company.objects.filter(year = year)
  #response = HttpResponse(mimetype='application/ms-excel')
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet("Companies List")
  row_num = 0
  columns = [
    (u"Company Name", 12000),
    (u"Category", 5000),
    (u"Year", 5000),
    (u"CTC_UG", 8000),
    (u"CTC_PG", 8000),	
    (u"CTC_PHD", 8000),
  ]
  font_style = xlwt.XFStyle()
  font_style.font.bold = True
  for col_num in xrange(len(columns)):
    ws.write(row_num, col_num, columns[col_num][0], font_style)
    # set column width
    ws.col(col_num).width = columns[col_num][1]
  font_style = xlwt.XFStyle()
  font_style.alignment.wrap = 1

  for c in cs:
    row_num += 1
    row = [
      str(c.name),
      str(c.category),
      str(c.year),
      str(c.package_ug),
      str(c.package_pg),
      str(c.package_phd)
    ]
    print row
    for col_num in xrange(len(row)):
      ws.write(row_num, col_num, row[col_num], font_style)
  wb.save('Companies Data - '+ year +'.xls')

#export_company_data_to_excel()
