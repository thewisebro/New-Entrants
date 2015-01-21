from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.forms.widgets import Select
from django.views.generic.base import TemplateView

from django.contrib import messages

import logging, re
import datetime

from core import forms
from api import model_constants as MC
from placement.forms import BaseModelFormFunction
from placement import forms, policy
from placement.models import *
from placement.policy import current_session_year
from placement.utils import *
from nucleus.models import StudentInfo

import settings

l = logging.getLogger('placement')

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/placement/'

# IMPORTANT : Objects of Student and PlacementStudent are to be stored in session.
# These objects are used in all the templates.

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def photo(request):
  try :
    l.info(request.user.username + ': Opened view to add/update photo')
    student = request.user.student
    plac_person = student.placementperson
    if request.method == 'POST' :
      # Form has been submitted.
      form = forms.Place(request.POST, request.FILES, instance = plac_person)
      if form.is_valid() :
        form.save()
        plac_person = PlacementStudent.objects.get(student = student)
        l.info(request.user.username + ': successfully added/updated photo')
        messages.success(request, 'Photo updated successfully.')
        return HttpResponseRedirect(reverse('placement.views.index'))
      else:
        messages.error(request, form.errors, extra_tags='form_error')
    else:
      # Form has not been submitted.
      form = forms.Place(instance = plac_person)
      if plac_person.photo :
        # Change the url of photo
        plac_person.photo.name = u'placement/photo/'
    return render_to_response('placement/basic_form.html', {
        'form':form,
        'title':'Photo',
        'action': reverse('placement.views_profiles.photo'),
        'editable_warning': 'Will not be editable once Locked.'
        }, context_instance=RequestContext(request))
  except Exception, e :
    l.info(request.user.username + ': Exception in adding/updating photo')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def personal_information(request):
  """
    View/Update Studental Information
  """
  try:
    l.info(request.user.username + ': Opened view to update StudentInfo')
    student = request.user.student
    try:
      info = StudentInfo.objects.get(student = student)
    except StudentInfo.DoesNotExist as e:
      # create a default entry
      b_d = datetime.date(1990,1,1)
      # TODO : find a better way to create default rown
      info = StudentInfo.objects.create(student = student, birth_date = b_d, height = 180, weight = 60)
      l.info(request.user.username + ': created a default entry in personinfo.')
    if request.method == 'POST':
      form = forms.Profile(request.POST, instance = info)
      form.student = student
      if form.is_valid() :
        form.student = student
        form.save()
        l.info(request.user.username + ': Updated StudentInfo successfully. Redirecting to home.')
        messages.success(request, 'Profile saved successfully')
        return HttpResponseRedirect(reverse('placement.views.index'))
      else:
        messages.error(request, form.errors, extra_tags='form_error')
    else :
      form = forms.Profile(instance = info)
    return render_to_response('placement/basic_form.html', {
        'form': form,
        'title': 'Studental Information',
        'action': reverse('placement.views_profiles.personal_information'),
        'editable_warning': 'Will not be editable once Locked.'
        }, context_instance=RequestContext(request))
  except Exception, e :
    l.info(request.user.username + ': Exception in updating personal information')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def contact(request):
  """
    View/Update Student.
  """
  try:
    l.info(request.user.username + ': Opened view to update Student')
    # Do not take student from session
    student = Student.objects.get(user = request.user)
    info = StudentInfo.objects.get_or_create(student = student)[0]
    if request.method == 'POST':
      form = forms.Contact(request.POST, instance = student)
      l.info(request.user.username + ': submitted student info.')
      # TODO : Use cleaned values from the form
      # this may lead to sql insertion!
      student.email_id = request.POST['email_id']
      student.personal_contact_no = request.POST['personal_contact_no']
      student.bhawan = request.POST['bhawan']
      student.room_no = request.POST['room_no']
      student.gender = request.POST['gender']
      info.home_contact_no = request.POST['permanent_contact_no']
      info.save()
      student.save()
      l.info(request.user.username + ': Updated Student successfully. Redirecting to home.')
      messages.success(request, 'Profile saved successfully')
      return HttpResponseRedirect(reverse('placement.views.index'))
    form = forms.Contact(instance=student, initial={'permanent_contact_no': info.home_contact_no})
    editables = ('email_id', 'personal_contact_no', 'bhawan', 'room_no', 'gender', 'permanent_contact_no')
    return render_to_response('placement/generic_locked.html', {
        'form': form,
        'title': 'Contact Information',
        'action': reverse('placement.views_profiles.contact'),
        'editables' : editables,
        }, context_instance=RequestContext(request))
  except Exception, e :
    l.info(request.user.username + ': Exception in updating personal information')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def educational_details(request):
  """
    View/Update Educational Details
  """
  try :
    l.info(request.user.username + ': Viewing Eduational Details')
    student = request.user.student
    plac_person = student.placementperson
    if plac_person.status in ('LCK', 'VRF') :
      EducationalDetailsFormSet = modelformset_factory(EducationalDetails, form=forms.ModelForm,
                                                       can_delete = False, extra = 0, exclude = ('student', ))
    else :
      EducationalDetailsFormSet = modelformset_factory(EducationalDetails, form=forms.ModelForm,
                                                       can_delete = True, exclude = ('student', ))
    if request.method == 'POST' :
      if plac_person.status in ('LCK', 'VRF') :
        # The user cannot update this information if he is locked/verified/opened. He can only edit it if it is closed or open
        return TemplateView(request, template="404.html")
      formset = EducationalDetailsFormSet(request.POST, queryset = EducationalDetails.objects.filter(student = student))
      if formset.is_valid() :
        instances = formset.save(commit = False)
        # Make sure that the last element has student attached to it as it may be a newly created instance
        if len(instances) > 0:
          instances[-1].student = student
        # save each instance individually as formset.save() will throw an exception if a form is marked as to be deleted.
        for instance in instances :
          instance.save()
        # Update the Student.cgpa field
        courses_order = zip(*MC.SEMESTER_CHOICES)[0] # Order of courses, higher index means a higher course
        highest_order = -1
        cgpa = None
        for detail in EducationalDetails.objects.filter(student = student) :
          current_order = courses_order.index(detail.course)
          if current_order > highest_order :
            highest_order = current_order
            cgpa = detail.cgpa
        if cgpa : # If the user has at least one row in database
          student.cgpa = cgpa
        else :
          student.cgpa = ''
        student.save()
        l.info(request.user.username + ': Updated Educational Details successfully.')
        messages.success(request, 'Updated the Educational Details')
        return HttpResponseRedirect(reverse('placement.views.index'))
    else :
      formset = EducationalDetailsFormSet(queryset = EducationalDetails.objects.filter(student = student))
    # Override the choices for course as per the course of the user.
    # Added the blank option to make sure that the formset works fine.
    if student.semester[:-2] == 'UG':
      for form in formset :
        form.fields['course'].choices = (('','---------'),) + MC.SEMESTER_CHOICES[3:19]
    if student.semester[:-2] == 'PG':
      for form in formset :
        form.fields['course'].choices = (('','---------'),) + MC.SEMESTER_CHOICES[3:5] + MC.SEMESTER_CHOICES[:3] + MC.SEMESTER_CHOICES[19:26]
    if student.semester[:-2] == 'PHD':
      for form in formset :
        form.fields['course'].choices = (('','---------'),) + MC.SEMESTER_CHOICES[:5]

    # Insert courses not offered by our institute as these are missing in the branch.
    branches = get_branches_for_educational_details()
    for form in formset :
      form.fields['discipline'].choices = branches
      form.fields['discipline'].widget = Select(choices = branches )

    if plac_person.status in ('LCK', 'VRF') :
      # The details are uneditable
      template = 'placement/generic_locked_set.html'
    else :
      template = 'placement/basic_form.html'
    return render_to_response(template , {
        'form' : formset,
        'title' : 'Educational Details',
        'action' : reverse('placement.views_profiles.educational_details'),
        'editable_warning': 'Will not be editable once Locked.',
        'educational_jquery_required' : True,
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Exception in editing educational details')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def placement_information(request) :
  """
    View/Update Placement Information
  """
  try :
    l.info(request.user.username + ': Update/View Placement Information')
    student = request.user.student
    plac_info, created = PlacementInformation.objects.get_or_create(student = student)
    if created :
      l.info(request.user.username + ': Created default PlacementInformation')
    plac_person = student.placementperson
    if request.method == 'POST' :
      if plac_person.status == 'LCK' :
        # User cannot edit anything
        return TemplateView(request, template="404.html")
      if plac_person.status == 'VRF' :
        # The student can update only editable fields
        # TODO : clean the fields
        plac_info.area_of_interest = request.POST['area_of_interest']
        plac_info.course_taken     = request.POST['course_taken']
        plac_info.save()
        messages.success(request, 'Updated Placement Information')
        return HttpResponseRedirect(reverse('placement.views.index'))
      form = BaseModelFormFunction(PlacementInformation, exclude_list = ('student', 'registration_no'),
                                   data = request.POST, instance = plac_info)
      if form.is_valid():
        instance = form.save(commit = False)
        instance.student = student
        instance.save()
        l.info(request.user.username + ': Updated Placement Information. Redirecting to home')
        messages.success(request, 'Updated Placement Information')
        return HttpResponseRedirect(reverse('placement.views.index'))
      else:
        messages.error(request, form.errors, extra_tags='form_error')
    else :
      form = BaseModelFormFunction(PlacementInformation, exclude_list = ('student', 'registration_no'), instance = plac_info)
    if plac_person.status in ('LCK', 'VRF') :
      # User can edit only certain fields
      template = 'placement/generic_locked.html'
    else :
      template = 'placement/basic_form.html'
    # Fields which are editable even when the student is verified.
    if plac_person.status == 'VRF' :
      editables = ('area_of_interest', 'course_taken')
    else :
      editables = None
    return render_to_response(template, {
        'form' : form,
        'title' : 'Placement Information',
        'action' : reverse('placement.views_profiles.placement_information'),
        'editables' : editables,
        'editable_warning': '"Area of Interest" and "Courses Taken" fields will be editable once Verified.'
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Exception in editing placement information')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def editset(request, model_name):
  """
  A view to handle all the formsets that are mapped to student using ForeignKey to student.
  It hides the student field and handles it when saving the formset.
  The input to this function is in the format 'placement_information' if you want it to render
  PlacementInformation ModelFormSet.
  """
  try :
    l.info (request.user.username + ': Entered Editset with model_name = ' + str(model_name))
    # To add an allowed formset, add it to the following list.
    # Only then the modelname can be passes to this function.
    allowed_models = ['ProjectInformation', 'InternshipInformation', 'JobExperiences',
                      'ExtraCurriculars', 'LanguagesKnown', 'ResearchPublications']
    student = request.user.student
    plac_person = student.placementperson
    action = model_name # the form will be submitted back to this view with this 'action'
    model_name_spaced = re.sub(r'_([a-z])', lambda pat: ' ' + pat.group(1).upper(), model_name.capitalize())
    # Remove underscores, make the first character after underscore capital, also make the first character capital
    model_name = re.sub(r'_([a-z])', lambda pat: pat.group(1).upper(), model_name.capitalize())
    if model_name not in allowed_models :
      l.info(request.user.username + ': Tried to edit ' + model_name + ', which is not allowed.')
      return TemplateView(request, template="404.html")
    if model_name == 'ProjectInformation':
      editable_warning = '"Description", "Proirity" and "Visible" fields will be editable once Verified'
    elif model_name == 'LanguagesKnown':
      editable_warning = 'Will not be editable once Locked'
    else:
      editable_warning = '"Proirity" and "Visible" fields will be editable once Verified'

    model_type = globals()[model_name]
    if plac_person.status in ('LCK', 'VRF') :
      FormSetFactory = modelformset_factory(model_type, form=forms.ModelForm,
                                            extra = 0, exclude = ('student', ))
    else :
      FormSetFactory = modelformset_factory(model_type, form=forms.ModelForm,
                                            can_delete = True, exclude = ('student', ))
    # Details which will be editable even if the student is locked or verified.
    # To make a field editable, just add the field name to the ediatbles tuple
    # for the specific model_name
    editables = None
    if plac_person.status == 'VRF' :
      # Only a few details are editable
      template = 'placement/generic_locked_set.html'
      if model_name != 'LanguagesKnown' :
        editables = ('priority', 'visible')
      if model_name == 'ProjectInformation' :
        editables = ('priority', 'visible', 'brief_description')
    elif plac_person.status == 'LCK' :
      # Nothing is editable
      template = 'placement/generic_locked_set.html'
    else :
      template = 'placement/basic_form.html'
    if request.method == 'POST':
      if plac_person.status in ('LCK', 'VRF') :  # Restricted edit options
        formset = FormSetFactory( queryset = model_type.objects.filter(student = student))
        instances = formset.save(commit = False)
        i = 0
        for instance in instances :
          for field in editables :
            try :
              field_value = request.POST['form-' + str(i) + '-' + field]
            except KeyError :
              # The key was not found. This may be due to the fact that the field
              # is a BooleanField and the user set it to false.
              field_value = False
            instance.__setattr__(field, field_value)
          i+=1
          instance.save()
        l.info (request.user.username + ': Update successfully- '+ model_name_spaced + '. Redirecting to home.')
        messages.success(request, 'Updated ' + model_name_spaced + '.')
        return HttpResponseRedirect(reverse('placement.views.index'))
      formset = FormSetFactory(request.POST, queryset = model_type.objects.filter(student = student))
      if formset.is_valid() :
        instances = formset.save(commit = False)
        if len(instances) > 0 :
          instances[-1].student = student
        # Save each instance individually as formset.save will throw exception if a form is marked as to be deleted.
        for instance in instances :
          instance.save()
        l.info (request.user.username + ': Update successfully- '+ model_name_spaced + '. Redirecting to home.')
        messages.success(request, 'Updated ' + model_name_spaced + '.')
        return HttpResponseRedirect(reverse('placement.views.index'))
    else :
      formset = FormSetFactory(queryset = model_type.objects.filter(student = student))
    return render_to_response(template , {
        'form' : formset,
        'editables' : editables,
        'title' : model_name_spaced,
        'action' : reverse('placement.views_profiles.editset', args=[action]),
        'editable_warning': editable_warning
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Exception in editing ' + str(model_name))
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def facebook(request) :
  """
  Show and edit the facebook details of the user.
  """
  try :
    l.info (request.user.username + ': Opened facebook.')
    student = request.user.student
    plac_person = student.placementperson
    if plac_person.status != 'VRF' :
      return TemplateView(request, template="404.html")
    try :
      facebook_content = Facebook.objects.get(student = student)
    except Facebook.DoesNotExist :
      facebook_content = None
    if request.method == 'POST' and policy.can_edit_facebook :
      form = BaseModelFormFunction(Facebook, exclude_list = ('student'), data = request.POST, instance = facebook_content)
      if form.is_valid() :
        instance = form.save(commit = False)
        instance.student = student
        instance.save()
        l.info (request.user.username + ': Updated facebook.')
        messages.success(request, 'Facebook details updated.')
        return HttpResponseRedirect(reverse('placement.views.index'))
      else:
        messages.error(request, form.errors, extra_tags='form_error')
    if student.branch.degree == 'M.Tech.':
      form = BaseModelFormFunction(Facebook, exclude_list = ('student'), instance = facebook_content)
    else:
      form = BaseModelFormFunction(Facebook, exclude_list = ('student', 'b_tech_degree'), instance = facebook_content)
    if policy.can_edit_facebook :
      # The details are uneditable
      template = 'placement/basic_form.html'
    else :
      template = 'placement/generic_locked.html'
    if student.branch.degree == 'M.Tech.':
      form.fields['internship'].label = 'Internship/Work Experience'
    return render_to_response(template , {
        'form' : form,
        'name' : 'facebook_form',
        'title': 'Facebook',
        'action' : reverse('placement.views_profiles.facebook')
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Exception in editing facebook.')
    l.exception(e)
    return handle_exc(e, request)
