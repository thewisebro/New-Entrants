import xlwt
from nucleus.models import *
#from nucleus.models import PersonInfo

#def generate_excel_from_list(filename, sheets, ):


def export():
  ps = Student.objects.filter(admission_year__lt=2016)
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
    try:
       info = StudentInfo.objects.get(student=p)
       cat = info.category
    except:
       cat = ''
    row_num += 1
    row = [
      str(p.user.username),
      str(p.name),
      str(p.branch.name),
      str(cat),
      str(p.user.gender)
    ]
    print row
    for col_num in xrange(len(row)):
      ws.write(row_num, col_num, row[col_num], font_style)
  wb.save('StudentsData_overall.xls')
  #return response
  #export_xls.short_description = u"Export XLS"

export()
