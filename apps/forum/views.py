from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from forum.models import *
from forum.forms import *
from django.utils import simplejson

@login_required
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

  return render(request,'forum/ask_question.html',{'form': form,})



def question_dict(question):
  return {
    'id': question.pk,
    'title': question.title,
    'description': question.description
  }

def answer_dict(answer):
  return {
    'id': answer.pk,
    'question_id': answer.question.pk,
    'description': answer.description
  }


def fetch_questions(request):
  questions = Question.objects.all()
  json_data = simplejson.dumps({'questions':map(question_dict, questions)})
  return HttpResponse(json_data, mimetype='application/json')

def fetch_question(request):
  question_id = request.GET['question_id']
  question = Question.objects.get(id=question_id)
  answers = Answer.objects.filter(question=question)
  json_data = simplejson.dumps({'question':question_dict(question),'answers':map(answer_dict,answers)})
  return HttpResponse(json_data, mimetype='application/json')


def add_answer(request):
  question_id = request.POST['question_id']
  description = request.POST['description']
  question = Question.objects.get(id=question_id)
  profile = Profile.get_profile(request.user.student)
  answer = question.answer_set.create(description=description, profile=profile)
  json_data = simplejson.dumps({'answer':answer_dict(answer)})
  return HttpResponse(json_data, mimetype='application/json')

def fetch_answer(request):
  answer_id = request.GET['answer_id']
  answer = Answer.objects.get(id=answer_id)
  json_data = simplejson.dumps({'answer':answer_dict(answer)})
  return HttpResponse(json_data, mimetype='application/json')

def follow_question(request):
  question_id = request.GET['question_id']
  question = Question.objects.get(id=question_id)
  profile = Profile.get_profile(request.user.student)
  profile.question_followed.add(question)
