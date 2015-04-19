from django.shortcuts import render
from django.contrib.auth.models import User
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from genforms.models import *
from genforms.forms import *

@login_required
def libform_view(request):
  user = request.user
  person = Student.objects.get(user=user)
  person_info = StudentInfo.objects.get_or_create(student=person)[0]
  first_time = True
  try:
    if LibForm.objects.get(person = person) is not None:
      first_time = False
  except:
    first_time = True

  grad_year=0
  editable=0
  if person.semester[:3]=="PHD":
    grad_year = int("20" + person.user.username[:2]) + 3
  else:
    grad_year = int("20" + person.user.username[:2]) + (person.branch.duration+1)/2
  if grad_year < date.today().year:
    editable=1
  print grad_year

  if person_info.fathers_name!='':
    fathers_or_guardians_name = person_info.fathers_name
  else:
    fathers_or_guardians_name = person_info.local_guardian_name
  if person_info.home_contact_no!='':
    home_parent_guardian_phone_no = person_info.home_contact_no
  elif person_info.fathers_office_phone_no!='':
    home_parent_guardian_phone_no = person_info.fathers_office_phone_no
  else:
    home_parent_guardian_phone_no = person_info.local_guardian_contact_no

  pic_instance = Pic.objects.get_or_create(person=request.user.student)[0]
  pic_form = PicModelForm(instance = pic_instance)

  context = {
    'enrollment_no' : user.username,
    'name' : person.name,
    'programme' : person.branch.degree + ' ' + person.branch.name,
    'department' : person.branch.get_department_display(),
    'pic_instance' : pic_instance,
    'pic_form' : pic_form,
    'first_time' : first_time,
    'editable' : editable,
    'error' : 0
  }
  if request.method == 'POST':                                          #On Pressing the Submit Button
    if first_time == True:                                              #If pressed for the first time
      form = LibModelForm(request.POST)
      if form.is_valid():
        libform = form.save(commit=False)
        libform.person = person
        reason = request.POST['reason']
        if reason=="Other":
          reason_value = request.POST['other-reason-value']
          libform.reason = reason_value
        else:
          libform.reason = reason
        libform.save()
        return HttpResponseRedirect('')
      else:
        context['error']=1;
        context['form'] = form
        return render(request, 'genforms/index.html', context)
    else:                                                              #If pressed to edit the existing object
      libform1 = LibForm.objects.get(person=person)
      form1 = LibModelForm(request.POST, instance=libform1)
      if form1.is_valid():
        libform_obj = form1.save(commit=False)
        reason = request.POST['reason']
        if reason=="Other":
          reason_value = request.POST['other-reason-value']
          libform_obj.reason = reason_value
        else:
          libform_obj.reason = reason
        libform_obj.save()
        return HttpResponseRedirect('')
      else:
        context['error']=1;
        context['form'] = form1
        return render(request, 'genforms/index.html', context)

  else:                                                                 #Display of the form

    if first_time == True:                                              #Display of fields from Student, StudentInfo table(the first time)
        print "hey1"
        data = {
          'permanent_address' : person_info.permanent_address,
          'pin_code' : person_info.pincode,
          'personal_contact_no' : person.user.contact_no,
          'fathers_or_guardians_name' : fathers_or_guardians_name,
          'home_parent_guardian_phone_no' : home_parent_guardian_phone_no,
          'blood_group': person_info.blood_group,
          'valid_till': date(grad_year, 6, 30),
          'birth_date' : person.user.birth_date,
        }
        print date(grad_year, 6, 30)
        form = LibModelForm(initial = data)
        context['form'] = form
        context['radio_id'] = "#spelling"
        context['other_radio_value'] = "null"
        return render(request, 'genforms/index.html', context)
    else:                                                                                 #Display of fields from existing object
        print "hey"
        libform1 = LibForm.objects.get(person=person)
        form1 = LibModelForm(instance = libform1)
        context['form'] = form1
        if(libform1.reason == "Spelling mistake"):
          context['radio_id'] = "#spelling"
        elif(libform1.reason == "Did not receive my smart card"):
          context['radio_id'] = "#unreceived"
        else:
          context['radio_id'] = "#other-radio"
          context['other_radio_value'] = libform1.reason

        return render(request, 'genforms/index.html', context)
