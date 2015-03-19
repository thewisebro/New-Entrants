import re

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template import RequestContext 
from django.db.models import Q

from nucleus.models import Branch
from facapp.models import *
# from facapp.utils import handle_exc
# from facapp.forms import BooksAuthoredForm, RefereedJournalPapersForm, PhotoUploadForm, ResumeUploadForm
# from api.forms import BaseForm, BaseModelForm, BaseModelFormFunction, ConfirmDeleteForm
# import pika
# from django.utils import simplejson
import json

# Create your views here.

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)  
def index(request):
  try:
    print 'yes'
    faculty = 'padamkk' # request.session['faculty']
    #photo_form = PhotoUploadForm()
    #resume_form = ResumeUploadForm()
    print 'yess'
    education = EducationalDetails.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    print '1'
    interests = Interests.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    print '2'
    professional_background = ProfessionalBackground.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    print '3'
    administrative_background = AdministrativeBackground.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    print '4'
    honors = Honors.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    teaching = TeachingEngagement.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    seminars = ParticipationSeminar.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    membership = Membership.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    misc = Miscellaneous.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    collaboration = Collaboration.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    books = BooksAuthored.objects.filter(faculty = faculty)
    refereed_papers = RefereedJournalPapers.objects.filter(faculty = faculty)
    research_projects = SponsoredResearchProjects.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    project_supervision = ProjectAndThesisSupervision.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    phd_supervised = PhdSupervised.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    organised_conferences = OrganisedConference.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    short_term_courses = ParticipationInShorttermCourses.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    special_lectures = SpecialLecturesDelivered.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    visits = Visits.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    rs_group = ResearchScholarGroup.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    invitations = Invitations.objects.filter(faculty = faculty, visibility = True).order_by('priority')
    print '5'
    return render(request,'facapp/index.html') # , {
        # 'interests': interests,
        # 'professional_background' : professional_background,
        # 'honors' : honors,
        # 'education' : education,
        # 'administrative_background' : administrative_background,
        # 'research_projects' : research_projects,
        # 'seminars' : seminars,
        # 'membership' : membership,
        # 'teaching' : teaching,
        # 'project_supervision' : project_supervision,
        # 'rs_group' : rs_group,
        # 'phd_supervised' : phd_supervised,
        # 'visits' : visits,
        # 'invitations' : invitations,
        # 'short_term_courses' : short_term_courses,
        # 'organised_conferences' : organised_conferences,
        # 'special_lectures' : special_lectures,
        # 'misc' : misc,
        # 'collaboration' : collaboration,
        # 'books' : books,
        # 'refereed_papers' : refereed_papers,
        # })
  except Exception as e:
    # Can't use handle_exc here because it redirects here. To avoid infinite loop, redirect to a static page.
    print 'Exception: ' + str(e)
    messages.error(request, 'Unknown error has occured. Please try again later. The issue has beeen reported')
    return render_to_response('error.html', {
        }, context_instance=RequestContext(request))

# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
# def add(request, model_name):
#   try:
#     faculty = request.session['faculty']
#     model_type = globals()[model_name]
#     if(model_name == 'Faculty'):
#       messages.error(request, 'Faculty can\'t be added.')
#       return HttpResponseRedirect(reverse('facapp.views.index'))
#     exclude_list = ['faculty',]
#     model_name_space_separated = re.sub(r"(?<=\w)([A-Z])", r" \1", model_name)
#     template_name = model_name_space_separated.lower().replace(' ', '_').strip() + '.html'
  
#     # If the form was submitted.
#     if request.method == 'POST':
#       form = BaseModelFormFunction(model_type, exclude_list, request.POST)
#       if form.is_valid():
#         # Get a model instance without committing the form.
#         new_entry = form.save(commit=False)
#         # Now fill the empty faculty field.
#         new_entry.faculty = faculty
#         # Now commit the model.
#         new_entry.save()
#         messages.success(request, model_name_space_separated + ' were successfully saved.')
#       else:
#         messages.error(request, form.errors, extra_tags='form_error')

#     # Direct to the details page.
#     form = BaseModelFormFunction(model_type, exclude_list)
#     new_list = list(model_type.objects.filter(Q(faculty=faculty)).order_by('priority'))
#     return render_to_response('facapp/' + template_name, {
#         'form': form,
#         'action': '/facapp/add/' + model_name + '/',
#         'list': new_list,
#         'model_name': model_name,
#         'model_name_space_separated': model_name_space_separated,
#         }, context_instance=RequestContext(request))
#   except Exception as e:
#     return handle_exc(e, request)

# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
# def update(request, model_name, instance_id):
#   try:
#     faculty = request.session['faculty']
#     model_type = globals()[model_name]
#     if(model_name == 'Faculty'):
#       exclude_list = ['user',]
#       old = model_type.objects.filter(pk=faculty.user)[0]  
#     else:
#       exclude_list = ['faculty',]
#       old = model_type.objects.filter(id=instance_id)[0]
#       # we are guaranteed that index out of range exception will not occur, if a valid instance_id was passed.
#     model_name_space_separated = re.sub(r"(?<=\w)([A-Z])", r" \1", model_name)
#     template_name = model_name_space_separated.lower().replace(' ', '_').strip() + '.html'
  
#     # If the form was submitted.
#     if request.method == 'POST':
#       # Build a new instance from old instance too.
#       form = BaseModelFormFunction(model_type, exclude_list, request.POST, files=request.FILES, instance=old)
#       if form.is_valid():
#         # Now commit the model.
#         form.save()
#         messages.success(request, model_name_space_separated + ' were successfully saved.')
#         # If Faculty then redirect to the home page.
#         if(model_name == 'Faculty'):
#           return HttpResponseRedirect(reverse('facapp.views.index'))
#         # For other redirect to the add page.
#         form = BaseModelFormFunction(model_type, exclude_list)
#         new_list = list(model_type.objects.filter(Q(faculty=faculty)).order_by('priority'))
#         return render_to_response('facapp/' + template_name, {
#             'form': form,
#             'action': '/facapp/add/' + model_name + '/',   # Add action.
#             'list': new_list,
#             'model_name': model_name,
#             'model_name_space_separated': model_name_space_separated,
#             }, context_instance=RequestContext(request))
#       else:
#         messages.error(request, form.errors, extra_tags='form_error')
    
#     # instance argument should not be empty.
#     form = BaseModelFormFunction(model_type, exclude_list, instance=old)
#     # Direct to the details page.
#     new_list = []
#     if(model_name != 'Faculty'):
#       new_list = list(model_type.objects.filter(Q(faculty=faculty)).order_by('priority'))
#     return render_to_response('facapp/' + template_name, {
#         'form': form,
#         'action': '/facapp/update/' + model_name + '/' + str(instance_id) + '/',  # Update action.
#         'list': new_list,
#         'model_name': model_name,
#         'model_name_space_separated': model_name_space_separated,
#         }, context_instance=RequestContext(request))
#   except Exception as e:
#     return handle_exc(e, request)

# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
# def delete(request, model_name, instance_id):
#   try:
#     faculty = request.session['faculty']
#     model_type = globals()[model_name]
#     if(model_name == 'Faculty'):
#       messages.error(request, 'Faculty can\'t be deleted.')
#       return HttpResponseRedirect(reverse('facapp.views.index'))
#     exclude_list = ['faculty',]
#     old = model_type.objects.filter(id=instance_id)[0]
#     model_name_space_separated = re.sub(r"(?<=\w)([A-Z])", r" \1", model_name)
#     template_name = model_name_space_separated.lower().replace(' ', '_').strip() + '.html'
  
#     # If the form was submitted.
#     if request.method == 'POST':
#       form = ConfirmDeleteForm(request.POST)
#       if form.is_valid():
#         yes_or_no = form.cleaned_data['choices']
#         if yes_or_no == 'Y':
#           old.delete()
#           messages.success(request, model_name_space_separated + ' was successfully deleted.')
#         else:
#           messages.success(request, 'Action was cancelled.')
#       else:
#         messages.error(request, form.errors, extra_tags='form_error')
#       # Direct to the add page.
#       form = BaseModelFormFunction(model_type, exclude_list)
#       new_list = list(model_type.objects.filter(Q(faculty=faculty)).order_by('priority'))
#       return render_to_response('facapp/' + template_name, {
#           'form': form,
#           'action': '/facapp/add/' + model_name + '/',
#           'list': new_list,
#           'model_name': model_name,
#           'model_name_space_separated': model_name_space_separated,
#           }, context_instance=RequestContext(request))

#     # If user clicked 'Delete' link then redirect him to a confirmation page.
#     form = ConfirmDeleteForm()
#     return render_to_response('facapp/' + template_name, {
#         'form': form,
#         'action': '/facapp/delete/' + model_name + '/' + str(instance_id) + '/',
#         'model_to_delete': old,
#         'model_name': model_name,
#         'model_name_space_separated': model_name_space_separated,
#         }, context_instance=RequestContext(request))
#   except Exception as e:
#     return handle_exc(e, request)

# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
# def publish(request):
#   try:
#     username = request.user.username
#     connection = pika.BlockingConnection(pika.ConnectionParameters(
#                 host='cms.channeli.in'))
#     channel = connection.channel()
#     channel.queue_declare(queue='publish_faculty_page_queue')
#     channel.basic_publish(exchange='',
#                 routing_key='publish_faculty_page_queue',
#                 body=username)
#     connection.close()
#     messages.success(request, 'Request sent successfully. Changes will be reflected soon!')
#     json = simplejson.dumps({})
#     return HttpResponse(json,mimetype='application/json')
#   except Exception as e:
#     print e
