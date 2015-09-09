import xlwt
from common.models import Person
#from nucleus.models import PersonInfo

#def generate_excel_from_list(filename, sheets, ):


def export():
  ps = StudentInfo.objects.filter(student__admission_year__lt=2016)
  #response = HttpResponse(mimetype='application/ms-excel')
  #response['Content-Disposition'] = 'attachment; filename=Students_UG_BArch_IV_19/8/2014.xls'
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet("Students")
  row_num = 0
  columns = [
    (u"Enrollment No", 5000),
    (u"Name", 12000),
    (u"Branch", 20000),
    (u"Category", 10000),
    (u"Gender", 5000),
  ]
  font_style = xlwt.XFStyle()
  font_style.font.bold = True
  for col_num in xrange(len(columns)):
    ws.write(row_num, col_num, columns[col_num][0], font_style)
    # set column width
    ws.col(col_num).width = columns[col_num][1]
  font_style = xlwt.XFStyle()
  font_style.alignment.wrap = 1

  for p in ps:
    #try:
      #pi = PersonInfo.objects.get(person=p)
    #except:
      #pass
    row_num += 1
    row = [
      str(p.student.user.username),
      str(p.student.name),
      str(p.student.branch.name),
      str(p.category),
      str(p.student.user.gender)
    ]
    for col_num in xrange(len(row)):
      ws.write(row_num, col_num, row[col_num], font_style)
  wb.save('StudentsData_overall.xls')
  #return response
  #export_xls.short_description = u"Export XLS"

