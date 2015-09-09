from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db import IntegrityError
from django.conf import settings
import logging, os
from django.views.generic.base import TemplateView
import datetime

from nucleus.models import Student, WebmailAccount
from placement import policy, forms
from placement.policy import current_session_year
from placement.models import *
from placement.utils import *

from django.contrib import messages


# XXX : Keep logged after all imports only
# As other imports might over write the logger
logger = logging.getLogger('placement')

l = logger

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/placement/'

# IMPORTANT : Objects of Student and PlacementPerson are to be stored in session.
# These objects are used in all the templates.

# Gateway to homepage.
# the user does not have to pass any test as this view handles itself
@login_required
def index(request):
  try :
    logger.info(request.user.username+": in homepage.")
    try:
      student = request.user.student
    except:
      if request.user.groups.filter(name = 'Placement Admin').exists() :
        # request.session['user']=request.user
        l.info(request.user.username+': Redirected to company.admin_list')
        return HttpResponseRedirect(reverse('placement.views_company.admin_list'))
      elif request.user.groups.filter(name = 'Placement Verify').exists() :
        l.info(request.user.username+': Redirected to verify.index')
        return HttpResponseRedirect(reverse('placement.views_verify.index'))
      elif request.user.groups.filter(name = 'Placement Department').exists() :
        dept_name = request.user.username[2:].upper()
        l.info(request.user.username+': Redirected to results.department')
        return HttpResponseRedirect(reverse('placement.views_results.department', args = [dept_name]))
      elif request.user.groups.filter(name = 'Student').exists() :
        l.info(request.user.username+': Redirected to Student Home')
        request.user.student = Student.objects.get(user = request.user)
      elif request.user.groups.filter(name = 'Faculty').exists() :
        l.info(request.user.username+': Redirected to Results Home')
        return HttpResponseRedirect(reverse('placement.views_results.company_list'))
      else :
        messages.error(request, 'You are not alloted any placement group. If you are elligible to visit this portal, contact IMG.')
        l.info(request.user.username+': Redirected to Channeli')
        return HttpResponseRedirect(reverse('nucleus.views.index'))
#        render_to_response('placement/error.html', context_instance=RequestContext(request))
    else:
    # XXX : Do not take student from session, at least home page should reflect the changes.
      student = Student.objects.get(user = request.user)
      plac_person = PlacementPerson.objects.get_or_create(student = student)[0]
      if (not WorkshopRegistration.objects.filter(placement_person=plac_person).exists()) and plac_person.status == 'VRF':
        l.info(request.user.username+': Redirected to Workshop Registration Page')
        return HttpResponseRedirect(reverse('placement.views_company.workshop_registration'))
      if plac_person.status == 'VRF' :
        applications = CompanyApplicationMap.objects.filter(plac_person = plac_person, company__year__contains = current_session_year())
      else :
        applications = None
      return render_to_response('placement/index.html', {
          'student' : student,
          'plac_person' : plac_person,
          'applications' : applications,
          }, context_instance=RequestContext(request))
  except Exception as e :
    print e
    logger.info(request.user.username+': got an exception.')
    logger.exception(e)
    # Can't use handle_exc here because it redirects here. To avoid infinite loop, redirect to a static page.
    messages.error(request, 'Unknown error has occured. Please try again later. The issue has beeen reported.')
    return render_to_response('placement/error.html', context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def resume(request) :
  """
  Current resume of the user.
  """
  try :
    student = request.user.student
    l.info (request.user.username+': Generated Resume')
    pdf = get_resume_binary(RequestContext(request), student, 'VER')
    if pdf['err'] :
      l.exception(request.user.username+': Error occured while generating resume')
      messages.error(request, 'An error occured while generating the PDF file.')
      return HttpResponseRedirect(reverse('placement.views.index'))
    response = HttpResponse(pdf['content'], content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Resume_' + student.user.username + '_' + sanitise_for_download(datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p')) + '.pdf'
    response['Content-Length'] = len(pdf['content'])
    return response
  except Exception as e :
    logger.info(request.user.username+': got an exception in generating resume.')
    logger.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def resume_nik(request) :
  """
  Current resume of the user.
  """
  try :
    student = request.user.student
    l.info (request.user.username+': Generated Resume')
    pdf = get_resume_binary(RequestContext(request), student, 'VER', False, True)
    if pdf['err'] :
      l.exception(request.user.username+': Error occured while generating resume')
      messages.error(request, 'An error occured while generating the PDF file.')
      return HttpResponseRedirect(reverse('placement.views.index'))
    response = HttpResponse(pdf['content'], content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Resume_' + student.user.username + '_' + sanitise_for_download(datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p')) + '.pdf'
    response['Content-Length'] = len(pdf['content'])
    return response
  except Exception as e :
    logger.info(request.user.username+': got an exception in generating resume.')
    logger.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def scorecard(request) :
  """
  Current scorecard of the user.
  """
  try :
    l.info (request.user.username+': Generated Scorecard')
    student = request.user.student
    pdf = get_scorecard_binary(RequestContext(request), student)
    if pdf['err'] :
      l.exception(request.user.username+': Error in generating Scorecard.')
      messages.error(request, 'An error occured while generating the PDF file.')
      return HttpResponseRedirect(reverse('placement.views.index'))
    response = HttpResponse(pdf['content'], content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Scorecard.pdf'
    response['Content-Length'] = len(pdf['content'])
    return response
  except Exception as e :
    logger.info(request.user.username+': got an exception in generating scorecard.')
    logger.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def apply(request, company_id) :
  """
  Applies to the specified company. Returns True if applied otherwise returns an error message.
  It is to be used via AJAX call.
  """
  try :
    company = get_object_or_404(Company, pk = company_id, year = current_session_year() )
    student = request.user.student
    # Do not pick plac_person from session as the plac_person might get updated
    # from django-admin
    plac_person = PlacementPerson.objects.get(student = student)
    if plac_person.status != 'VRF' :
      return HttpResponse('You are not elligible for placements.')
    msg = policy.can_apply(plac_person, company)
    if msg != True :
      # The user cannot apply to the company
      return HttpResponse(msg)
    try:
      company_req = float(company.cgpa_requirement)
    except:
      company_req = 0
    student_cgpa_queryset = EducationalDetails.objects.filter(student = student, course__startswith = student.branch.graduation)
    if not student_cgpa_queryset:
      student_cgpa = 0
    else:
      student_cgpa = student_cgpa_queryset.order_by('-course')[0].cgpa
    if company_req > float(student_cgpa):
      l.info(request.user.username +' applying to company having higher CGPA requirements.')
      return HttpResponse("You can not apply to this company as it has higher CGPA requirements.")
    if company.category_required:
      pdf = get_resume_binary(RequestContext(request), student, company.sector, category_required=company.category_required)
    else:
      pdf = get_resume_binary(RequestContext(request), student, company.sector)
    if pdf['err'] :
      return HttpResponse('Your resume cannot be generated. Please contact IMG immediately.')
    filepath = os.path.join(settings.MEDIA_ROOT, 'placement', 'applications', 'company'+str(company_id), str(student.user.username)+'.pdf')
    # Make sure that the parent directory of filepath exists
    parent = os.path.split(filepath)[0]
    if not os.path.exists(parent) :
      os.makedirs(parent)
    resume = open(filepath, 'w')
    resume.write(pdf['content'])
    resume.close()
    application = CompanyApplicationMap()
    application.plac_person = plac_person
    application.company = company
    application.status = 'APP'
    try :
      application.save()
      l.info(request.user.username+': Applied to '+company.name)
      return HttpResponse("True")
    except IntegrityError as ie:
      logger.exception(ie)
      ### Verify with Sandeep once. ###
      #os.remove(filepath)
      return HttpResponse('You have already applied to '+company.name)
    except Exception as e:
      logger.exception(e)
      ### Verify with Sandeep once. ###
      #os.remove(filepath)
      return HttpResponse(e)
  except Exception as e :
    logger.info(request.user.username+': got an exception in applying to ')
    logger.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def withdraw(request, company_id) :
  """
  Withdraws application from the company. Returns True if the application was withdrawn.
  Otherwise the error message is returned. It is to be used via AJAX call.
  """
  try :
    company = get_object_or_404(Company, pk = company_id, year = current_session_year() )
    student = request.user.student
    plac_person = request.user.student.placementperson
    try :
      application = CompanyApplicationMap.objects.get(company = company, plac_person = plac_person)
    except CompanyApplicationMap.DoesNotExist:
      return HttpResponse('You have not applied to '+company.name)
    if not application.status == 'APP' :
      # The application has been forwarded to the company.
      return HttpResponse('You cannot withdraw your application from '+ company.name)
    if not company.status == 'OPN':
      return HttpResponse('You cannot perform this action as '+ company.name +' application is closed')
    filepath = os.path.join(settings.MEDIA_ROOT, 'placement', 'applications', 'company'+str(company_id), str(student.user.username)+'.pdf')
    try :
      os.remove(filepath)
      application.delete()
      l.info(request.user.username+': Withdrew from '+company.name)
    except Exception as e:
      l.exception(e)
      return HttpResponse(e)
    return HttpResponse('True')
  except Exception as e :
    logger.info(request.user.username+': got an exception in withdrawing from '+company.name)
    logger.exception(e)
    return handle_exc(e, request)

# Forum views
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin')).exists(), login_url=login_url)
def forum(request, forum_type, page_no = None) :
  """
  Show all the posts to the technical/placement forums.
  It saves the reply to a post also.
  """
  try :
    l.info(request.user.username+': Viewed Forum')
    if request.method == 'POST' :
      # This view saves the replies to threads also.
      # This is useful as the same page number can be displayed without
      # much effort(Paging).
      if request.POST['content']=="":
        messages.error(request, 'An empty reply cannot be posted')
        return HttpResponseRedirect(reverse('placement.views.forum', args=[ forum_type ]))
      elif request.user.groups.filter(name='Student').exists():
        student = request.user.student
        post = ForumPost.objects.get(pk = request.POST['post_id'])
        ForumReply.objects.create(post = post,
                                enrollment_no = student.user.username,
                                person_name = student.name,
                                content = request.POST['content'],
                                )
      elif request.user.groups.filter(name='Placement Admin').exists():
        post = ForumPost.objects.get(pk = request.POST['post_id'])
        ForumReply.objects.create(post = post,
                                enrollment_no = '00000000',
                                person_name = 'Placement Admin',
                                content = request.POST['content'],
                                )
      l.info(request.user.username+': Posted Reply in forum.')
      return HttpResponseRedirect('')
    if not page_no :
      page_no = 1
    else :
      page_no = int(page_no)
    post_headers = ForumPost.objects.filter(forum_type = forum_type).order_by('-date')
    pages = range(1,(post_headers.count()+19)/10)
    # If only a single page, do not show paging
    if len(pages) == 1 :
      pages = None
    post_headers = post_headers[(page_no-1)*10:page_no*10]
    replies = []
    for post in post_headers :
      replies.append(ForumReply.objects.filter(post = post).order_by('date'))
    posts = zip(post_headers, replies)
    return render_to_response('placement/forums_view.html', {
        'forum_type' : forum_type,
        'posts' : posts,
        'page_no' : page_no,
        'pages' : pages
        }, context_instance = RequestContext(request))
  except Exception as e :
    logger.info(request.user.username+': got an exception in ' + forum_type + ' forum page_no ' + str(page_no))
    logger.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin')).exists(), login_url=login_url)
def forum_post(request) :
  """
  Adds a new Post to the forum.
  """
  try :
    if request.POST['title']=="":
      messages.error(request, 'Please fill in the Question before submitting.')
      return HttpResponseRedirect(reverse('placement.views.forum', args=[ request.POST['forum_type'] ]))
    elif request.method == 'POST' :
      if not request.user.groups.filter(name='Student'):
        student = request.user.student
        ForumPost.objects.create(enrollment_no = student.user.username,
                               person_name = student.user.name,
                               discipline_name = student.branch.name,
                               department_name = student.branch.get_department_display(),
                               title = request.POST['title'],
                               content = request.POST['content'],
                               forum_type = request.POST['forum_type']
                               )
      elif request.user.groups.filter(name='Placement Admin'):
        ForumPost.objects.create(enrollment_no = '00000000',
                               person_name = 'Placement Admin',
                               discipline_name = 'Admin',
                               department_name = 'Admin',
                               title = request.POST['title'],
                               content = request.POST['content'],
                               forum_type = request.POST['forum_type']
                               )

      try:
        student = request.user.student
        forum_type=request.POST['forum_type']
        if(forum_type=="T"):
          subject_mail="New forum post on technical forum by "+ student.user.name
        elif(forum_type=="P"):
          subject_mail="New forum post on placement forum by "+ student.user.name
        content_mail="Post Title: "+request.POST['title']+'\n'+"Post Content: "+request.POST['content']

        from django.core.mail import send_mail
        forum_type=request.POST['forum_type']
        if(forum_type=="T"):
          send_mail(subject_mail, content_mail, 'img@iitr.ernet.in' , ['img.placement@gmail.com'], fail_silently=True)
        elif(forum_type=="P"):
          send_mail(request.POST['title'], request.POST['content'], 'img@iitr.ernet.in' , ['placement.iitr@gmail.com'], fail_silently=True)
        messages.success(request, 'You posted successfully on the forum')

      except Exception as e:
        logger.info(request.user.username+': got an exception in mailer block during forum post')
        logger.exception(e)
        return handle_exc(e, request)

      return HttpResponseRedirect(reverse('placement.views.forum', args=[ request.POST['forum_type'] ]))
    else :
      return TemplateView(request, template="404.html")
  except Exception as e :
    logger.info(request.user.username+': got an exception in forums')
    logger.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def toggle(request):
  """
    Option for PhD Students to toggle their status from Open to Closed and vice versa, until it is verified
  """
  l.info(request.user.username+': tried to change placement status.')
  student = request.user.student
  # Do not pick plac_person from session as the plac_person might get updated
  # from django-admin
  plac_person = PlacementPerson.objects.get(student = student)
  if student.branch.graduation <> 'PHD':
    l.info(request.user.username+': not allowed to change status')
    return HttpResponse('You are not allowed to perform this operation. This has been reported.')
  elif plac_person.status not in ['OPN', 'LCK']:
    l.info(request.user.username+': not allowed to change status')
    return HttpResponse('You are not allowed to perform this operation. This has been reported.')
  fin = None
  if plac_person.status == 'LCK':
    plac_person.status = 'OPN'
    fin = 'Opened'
  elif plac_person.status == 'OPN':
    plac_person.status = 'LCK'
    fin = 'Locked'
  else:
    return HttpResponse('You are not allowed to perform the operation.')
  plac_person.save()
  l.info(request.user.username + ': changed the status to ' + fin)
  return HttpResponse('Your placement status has been changed successfully to \'' + fin + '\'')
