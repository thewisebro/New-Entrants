from django.shortcuts import render
from django.http import HttpResponse
from forum.models import *
from forum.forms import *

def ask_question(request):
  if request.method == 'POST':
    form = Ask_Question_Form(request.POST)
    if form.is_valid():
      new_question = form.save(commit=False)
      new_question.profile = Profile.get_profile(request.user.student)
      new_question.save()
      return  HttpResponse("Question added")

  else:
    form = Ask_Question_Form()

  return render(request, 'forum/ask_question.html', {'form': form,})
