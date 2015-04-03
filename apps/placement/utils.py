from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.template.loader import render_to_string

from xhtml2pdf import pisa

import cStringIO as StringIO
import logging, os


from placement.models import *
from api import model_constants as MC
from placement.constants import PAY_PACKAGE_CURRENCY_CONVERSION_RATES
from placement.policy import current_session_year
from nucleus.models import StudentInfo, Branch

from django.conf import settings

l = logging.getLogger('channel-i_logger')

##########################################################################
# This module is for utility functions, no logs should be generated here #
# for normal operations. Error and important logs can be made by these   #
# functions but info logs must be handled in the calling function only.  #
##########################################################################

def handle_exc(e, request, text=None):
  l.error(e)
  if isinstance(e, Http404) :
    # TODO : do whatever you wanna do here, you may display a message or a 404 page
    raise Http404
  if text:
    messages.error(request, text)
  else:
    messages.error(request, 'Unknown error has occured. Please try again later. The issue has beeen reported.')
  return HttpResponseRedirect(reverse('placement.views.index'))

def sanitise_for_download(string):
  """
  Sanitises filenames for download purposes. Some characters like spaces, commas, semicolons might cause problem
  in the headers so they need to be removed.
  """
  return string.replace(' ', '-').replace(',','_').replace(':', '_')

def get_resume_binary(context, student, resume_type, verification_resume = False, is_reduced = False, photo_required = False) :
  """
  Returns dictionary of the resume for the specified student.
  Keys of the dictionary are 'err' and 'content'.
  'content' is resume encode in pdf binary format.
  Returned string can be saved in a file as pdf document or can be rendered
  in a HttpResponse to the client.
  resume_type can be either 'VER' (for full resume) or any value from
  placement.constants.COMPANY_RESUME_CHOICES
  verification_resume : whether to display all visible and hidden information.
  """
  plac_person, created = PlacementPerson.objects.get_or_create(student = student)
  if created :
    l.info('Utils : Created default PlacementInformation for ' + student.user.username + ' as his/her resume was requested.')
  year = current_session_year()
  if verification_resume :
    internships = InternshipInformation.objects.filter(student = student).order_by('priority')
    projects = ProjectInformation.objects.filter(student = student).order_by('priority')
    publications = ResearchPublications.objects.filter(student = student).order_by('priority')
    job = JobExperiences.objects.filter(student = student).order_by('priority')
    extra = ExtraCurriculars.objects.filter(student = student).order_by('priority')
  else :
    internships = InternshipInformation.objects.filter(student = student, visible = True).order_by('priority')
    projects = ProjectInformation.objects.filter(student = student, visible = True).order_by('priority')
    publications = ResearchPublications.objects.filter(student = student, visible = True).order_by('priority')
    job = JobExperiences.objects.filter(student = student, visible = True).order_by('priority')
    extra = ExtraCurriculars.objects.filter(student = student, visible = True).order_by('priority')
  try:
    plac_info = PlacementInformation.objects.get(student = student)
    achievements = plac_info.achievements
  except PlacementInformation.DoesNotExist as e:
    plac_info = None
    achievements = None
  educations = []
  graduation = student.branch.graduation
  # Run the queries separately to preserve the required order
  if graduation == 'UG' :
    courses = ('DPLM' ,'12TH' ,'10TH')
  elif graduation == 'PG' :
    courses = ('UG0' ,'DPLM' ,'12TH' ,'10TH' ,'PG0')
  elif graduation == 'PHD' :
    courses = ('PG0' ,'UG0' ,'DPLM' ,'12TH' ,'10TH')
  course_name_map = {}
  for (code,name) in MC.SEMESTER_CHOICES :
    course_name_map[code] = name
  ed_current = EducationalDetails.objects.filter(student = student, course__startswith = graduation).order_by('-course')
  if ed_current.exists() :
    # For current course, we have to show the degree (B.Tech., M.Tech., MURP etc) and not just UG or PG
    # It will look like - 'B.Tech. 3rd Year'
    if not graduation == 'PHD' :
      # Do not compute course if PHD student
      year = ed_current[0].course[2]
      course_name = student.branch.degree
      if year == '1' :
        course_name += ' 1st '
      elif year == '2' :
        course_name += ' 2nd '
      elif year == '3' :
        course_name += ' 3rd '
      else :
        course_name += ' ' + year + 'th '
      course_name += 'Year'
    else :
      course_name = course_name_map[ed_current[0].course]
    educations.append((ed_current[0], course_name))
  for course in courses :
    more_details = EducationalDetails.objects.filter(student = student, course = course)
    for detail in more_details :
      educations.append((detail, course_name_map[detail.course]))
  e = EducationalDetails.objects.filter(student=student, course='UG0')
  if e.exists() and e[0].discipline!='NOT' :
    if e[0].discipline == 'NA' :
      ug_name = 'Not Applicable'
    else :
      b = Branch.objects.get(code=e[0].discipline)
      ug_name = b.name
  else:
    ug_name = ''
  languages = LanguagesKnown.objects.filter(student = student)
  try:
    info = StudentInfo.objects.get(student = student)
  except StudentInfo.DoesNotExist as e:
    info = None
  template_name = 'placement/resume.html'
  if is_reduced :
    template_name = 'placement/resume_nik.html'
  display = True #whether to display registration no
  if plac_person.status == 'CLS':   #alumni check?
    display = False
  registration_no  = student.branch.degree + '/' + student.branch.code + '/' + student.user.username + '/'
  year = current_session_year() + 1
  registration_no += str(year)
  html  = render_to_string(template_name,
                           { 'pagesize' : 'A4',
                             'plac_person' : plac_person,
                             'internships' : internships,
                             'projects' : projects,
                             'education' : educations,
                             'plac_info' : plac_info,
                             'languages' : languages,
                             'extra' : extra,
                             'info' : info,
                             'year': year,
                             'display' : display,
                             'jobs' : job,
                             'achievements' : achievements,
                             'publications' : publications,
                             'verification_resume' : verification_resume,
                             'ug_name' : ug_name,
                             'registration_no' : registration_no,
                             'photo_required' : photo_required,
                             }, context_instance = context)
  result = StringIO.StringIO()
  # The link of photo is placement/photo/, so we need to convert it to /home/.../photo/file.jpg
  # so that the pisa library can embed it in the pdf file.
  def fetch_resources(uri, rel):
    if uri == reverse('placement.media.photo') :
      return os.path.join(settings.MEDIA_ROOT,
                          uri.replace(settings.MEDIA_URL, ""),
                          plac_person.photo.path
                          )
    else :
      return os.path.join(settings.PROJECT_ROOT,
                          'static',
                          uri.replace(settings.STATIC_URL, '')
                          )
  pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, link_callback=fetch_resources )
  reply = {'err' : pdf.err,
           'content' : result.getvalue()
           }
  return reply

def get_scorecard_binary(context, student) :
  """
  Returns dictionary of the scorecard for the specified student.
  Keys of the dictionary are 'err' and 'content'.
  'content' is scorecard encode in pdf binary format.
  Returned string can be saved in a file as pdf document or can be rendered
  in a HttpResponse to the client.
  """
  try :
    registration_no = PlacementInformation.objects.get(student = student).registration_no
  except PlacementInformation.DoesNotExist :
    registration_no = None
  # order is important, that's the only reason we are firing multiple queries
  if not registration_no:
    registration_no  = student.branch.degree + '/' + student.branch.code + '/' + student.user.username + '/'
    year = current_session_year() + 1
    registration_no += str(year)
  print registration_no
  courses = ('10TH', '12TH', 'UG', 'DPLM', 'PG', 'PHD')
  educational_details = []
  for course in courses :
    more_details = EducationalDetails.objects.filter(student = student, course__startswith = course).order_by('course')
    educational_details.extend(more_details)
  course_name_map = {}
  for (code,name) in MC.SEMESTER_CHOICES :
    course_name_map[code] = name
  discipline_map = {}
  for (code, name) in get_branches_for_educational_details() :
    discipline_map[code] = name
  details = []
  for detail in educational_details :
    if detail.discipline == 'NOT' :
      discipline = detail.discipline_provided
    else :
      discipline = discipline_map[detail.discipline]
    details.append((detail, course_name_map[detail.course], discipline))
  html  = render_to_string('placement/scorecard.html',
                           { 'pagesize' : 'A4',
                             'student' : student,
                             'registration_no' : registration_no,
                             'details' : details,
                             }, context_instance = context)
  result = StringIO.StringIO()
  pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
  reply = {'err' : pdf.err,
           'content' : result.getvalue()
           }
  return reply

def get_ctc(currency_field) :
  """
  returns the amount of the currency field in INR
  """
  #space_at = currency_field.find(' ')
  #amount = int(currency_field[ : space_at])
  chunks = currency_field.split(' ')
  if len(chunks) < 2 :
    return 0
  if chunks[1] == 'Lacs':
    amount = float(chunks[0])*100000
  elif chunks[1] == 'Thousands':
    amount = float(chunks[0])*1000
  #currency = currency_field[space_at + 1 : ]
  currency = chunks[2]
  amount = int(amount)
  return amount * PAY_PACKAGE_CURRENCY_CONVERSION_RATES[currency]

def get_branches_for_educational_details() :
  """
  returns a tuple of branch code and branch name with three extra entries,
  1: blank, 2:NA/Not Applicable, 3:NOT/None Of These
  """
  branches = [(''   , '--------------'),
              ('NA' , 'Not Applicable'),
              ('NOT', 'None of these' )]
  branches.extend( Branch.objects.values_list('code', 'name').order_by('name') )
  return branches

####################### Validators ########################

def ContactValidator(value):
  if not str(value).isdigit():
    raise ValidationError("Contact number should contain only numerical digits.")
