# python imports
import cStringIO as StringIO
import datetime
import logging, traceback
import math
import os
import pdb
import json

# django imports
from django import forms
from django.conf import settings
from django.db.models import Max, Sum, Min, Q
from django.core.urlresolvers import reverse
from django.http import HttpResponse , HttpResponseRedirect, HttpRequest
from django.http import Http404
from django.shortcuts import render_to_response, get_list_or_404
from django.template import Context
from django.template.context import RequestContext
from django.template.loader import render_to_string, get_template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.context_processors import csrf

# libraries
from xhtml2pdf import pisa

# models
from messmenu.models import Menu

# local imports
from api.model_constants import BHAWAN_CHOICES
from messmenu.utils.utils import get_monday_date
from messmenu.utils.views_common import add_common_functionality

root = os.getenv("HOME")

#### 'bhawan' refers to bhawan code
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').count() != 0)
def index(request, bhawan = None, week = 0, pdf = None):
  logger = logging.getLogger(__name__)
  if pdf and pdf != 'pdf':
    raise Http404
  fixed_params = add_common_functionality(request)

  week = int(week)
  if week < -2 or week > 2:
    raise Http404
  date = get_monday_date(week)
  ## date contains date of monday of the requested week
  bhawans = dict(BHAWAN_CHOICES)
  try:
    try:
      request.user.student
    except:
      raise HttpResponseRedirect('/')
  except:
    request.user.student = None
  if not bhawan:
    try:
      if request.user.student.bhawan and request.user.student.bhawan != 'NA':
        bhawan = request.user.student.bhawan
      else:
        ## bhawan not set
        bhawan = bhawans.iterkeys().next()
    except:
      print traceback.format_exc()
      logger.error(traceback.format_exc())
      ## if it fails to retrieve bhawan anyhow
      bhawan = 'RVB'
  try:
    print bhawan, date, date + datetime.timedelta(days = 6)

    for i in range(0,7):
      for j in range(1,4):
        menu = Menu.objects.filter(bhawan = bhawan, date = date + datetime.timedelta(i),time_of_day=j)
        if not menu:
          Menu.objects.create(bhawan = bhawan, date = date + datetime.timedelta(i),time_of_day=j,content='')

    menu = Menu.objects.filter(
                            bhawan = bhawan,
                            date__gte = date,
                            date__lte = date + datetime.timedelta(days = 6)
                            )
           
  except:
    print traceback.format_exc()
    logger.error(traceback.format_exc())
    raise Http404
    
  params_dict = {
    'menu': menu,
    'bhawans': bhawans,
    'bhawan': bhawan,
    'date': date,
    'week': week,
    'pdf': pdf,
  }
  params_dict.update(fixed_params)

  if not pdf:
    return render_to_response('messmenu/display_menu.html',
                              params_dict,
                              context_instance = RequestContext(request))
  else:
    template = get_template('messmenu/display_menu.html')
    context = Context(params_dict)    
    html = template.render(context)

    """
    a = settings.PROJECT_ROOT + settings.STATIC_URL + 'css/messmenu/main.css'
    print a
    b = open(a, 'r').read()
    print b
    #html += b
    print '\n\n', html, '\n\n', '________________\n\n'

    f = open('', 'w+b')
    f.write(str(html))
    f.close()   
    
    from tempfile import mkstemp

    # write html to a temporary file
    # can used NamedTemporaryFile if using python 2.6+
    fid, fname = mkstemp(dir='/tmp')
    print '..', fname, '..'
    f = open(fname, 'w+b')
    f.write(str(html))
    f.close()

    # now create pdf from the html 
    cmd = 'xhtml2pdf "%s"' % fname
    os.system(cmd)
    os.unlink(fname)

    # get the content of the pdf
    filename = fname+'.pdf'
    pdf = open(filename, 'r')
    content = pdf.read()

    pdf.close()
    os.unlink(pdf.name)

    response = HttpResponse(content, content_type='application/pdf')
    """
    
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('UTF-8')), 
                            dest = result, 
                            link_callback = fetch_resources)
    if pdf.err :
      logger.info(request.user.username + ': Error in PDF generation of %s' % bhawan)
      return HttpResponse('An error occured while generating the PDF file.')
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    filename = bhawan + '_' + str(date) + '_mess_menu'
    #filename = filename.replace(' ', '-')    
    response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'
    response['Content-Length'] = len(result.getvalue())
    return response


def fetch_resources(uri, rel):
  path = os.path.join(settings.PROJECT_ROOT,
                      'static',
                      uri.replace(settings.STATIC_URL, '')
         )
  return path

def menu_dict(menu):
  return {
    'time_of_day': menu.time_of_day,
    'content': ', '.join(map(lambda c:c.title(),filter(lambda a:a, menu.content.replace(
                       '\r','').split('\n'))))
  }

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').count() != 0)
def todays_menu(request):
  bhawan = request.user.student.bhawan
  menus = Menu.objects.filter(bhawan=bhawan, date=datetime.date.today()).exclude(content='')
  print menus
  json_data = json.dumps(map(menu_dict, menus))
  return HttpResponse(json_data, content_type='application/json')
