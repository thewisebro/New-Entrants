from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from nucleus.models import Student
from messmenu.models import Feedback
from messmenu.forms import FeedbackForm

import datetime

BHAWAN_CHOICES = {
    'AZB':'Azad Bhawan',
    'CTB':'Cautley Bhawan',
    'GNB':'Ganga Bhawan',
    'GVB':'Govind Bhawan',
    'JWB':'Jawahar Bhawan',
    'RKB':'Radhakrishnan Bhawan',
    'RJB':'Rajendra Bhawan',
    'RGB':'Rajiv Bhawan',
    'RVB':'Ravindra Bhawan',
    'MVB':'Malviya Bhawan',
    'SB':'Sarojini Bhawan',
    'KB':'Kasturba Bhawan',
    'IB':' Indra Bhawan',
    'DAY':'Day Scholar',
    'KIH':'Khosla International House',
    }

@login_required
def feedback(request):
  user = request.user
  try:
    person = Student.objects.get(user=user)
    bhawan = BHAWAN_CHOICES[person.bhawan]
    if request.method == 'POST':
      room_no = request.POST['room_no']
      rating = int(request.POST['rating'])
      if room_no:
        person.room_no = room_no
      person.save()
      feedbacks = Feedback.objects.filter(person=person)
      if not feedbacks:
        feedback = Feedback.objects.create(person=person)
        if rating:
          feedback.rating = rating
        feedback.save()
      else:
        already_rated = False
        current_month = datetime.datetime.now().month
        for feedback in feedbacks:
          if feedback.date_created.month == current_month:
            already_rated = True
        if already_rated:
          return render_to_response('messmenu/feedback.html',{
          'person':person,
          'already_rated':already_rated,
          },context_instance=RequestContext(request))
        else:
          feeback = Feedback.objects.create(person=person)
          if rating:
            feedback.rating = rating
          feedback.save()
      return render_to_response('messmenu/feedback.html',{
        'person':person,
        'already_rated':True,
        },context_instance=RequestContext(request))
    else:
      feedbacks = Feedback.objects.filter(person=person)
      already_rated = False
      if feedbacks:
        current_month = datetime.datetime.now().month
        for feedback in feedbacks:
          if feedback.date_created.month == current_month:
            already_rated = True
      if not already_rated:
        data = {}
        data['room_no'] = person.room_no
        data['rating'] = 0
        form = FeedbackForm(initial=data)
        return render_to_response('messmenu/feedback.html',{
          'person':person,
          'feedback_form':form,
          'bhawan':bhawan,
          },context_instance=RequestContext(request))
      else:
        return render_to_response('messmenu/feedback.html',{
          'person':person,
          'already_rated':already_rated,
          },context_instance=RequestContext(request))
  except Exception as e:
    return HttpResponseRedirect('/')
