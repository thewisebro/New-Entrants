from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from forum.models import *
from forum.forms import *
from django.utils import simplejson
from core.models import Count,Q
from taggit.models import Tag,TaggedItem

@login_required
def ask_question(request):
  if request.method == 'POST':
    form = Ask_Question_Form(request.POST)
    if form.is_valid():
      print request.POST['tags']
      new_question = form.save(commit=False)
      new_question.profile = Profile.get_profile(request.user.student)
      new_question.save()
      form.save_m2m()
      return  HttpResponse("Question added")

  else:
    form = Ask_Question_Form()

  return render(request,'forum/ask_question.html',{'form': form,})



def answer_dict(answer,profile):
  if profile.answers_up.filter(id=answer.pk).exists():
    upvote_bool = "true"
  else:
    upvote_bool = "false"
  if profile.answers_down.filter(id=answer.pk).exists():
    downvote_bool = "true"
  else:
    downvote_bool = "false"
  if profile == answer.profile:
    same_profile = "true"
  else:
    same_profile = "false"

  upvote_count = len(ProfileAnswerUpvoted.objects.filter(answer=answer))
  return {
    'id': answer.pk,
    'question_id': answer.question.pk,
    'description': answer.description,
    'upvote': upvote_bool,
    'downvote': downvote_bool,
    'same_profile': same_profile,
    'upvote_count': upvote_count
  }


def question_dict(question,profile):
  if profile.questions_followed.filter(id=question.pk).exists():
    follow_bool = "true"
  else:
    follow_bool = "false"
  if profile == question.profile:
    same_profile = "true"
  else:
    same_profile = "false"
  return {
    'id': question.pk,
    'title': question.title,
    'description': question.description,
    'follow_unfollow': follow_bool,
    'same_profile': same_profile,
  }

def tag_dict(tag,profile):
  if profile.tags_followed.filter(id=tag.pk).exists():
    follow_bool = "true"
  else:
    follow_bool = "false"
  return {
    'name': tag.name,
    'follow_unfollow': follow_bool
  }

def tag_name(tag):
  return tag.name

def tagitem_content(tagitem,profile):
  return tagitem.content_object

def activity_dict(activity,profile):
  if activity.activity_type == 'FOL_QUES':
    obj = question_dict(activity.content.question, profile)
    student_name = activity.content.profile.student.name
  elif activity.activity_type == 'UP_ANS':
    obj = answer_dict(activity.content.answer, profile)
    student_name = activity.content.profile.student.name
  elif activity.activity_type == 'ASK_QUES':
    obj = question_dict(activity.content, profile)
    student_name = activity.content.profile.student.name
  elif activity.activity_type == 'POST_ANS':
    obj = answer_dict(activity.content, profile)
    student_name = activity.content.profile.student.name
  else:
    obj = tag_dict(activity.content.tag, profile)
    student_name = activity.content.content_object.student.name
  return {
    'activity_type': activity.activity_type,
    'object_id': activity.object_id,
    'object': obj,
    'student_name': student_name
  }

def fetch_questions(request):
  questions = Question.objects.all()
  profile = Profile.get_profile(request.user.student)
  json_data = simplejson.dumps({'questions':map(lambda q:question_dict(q, profile), questions)})
  return HttpResponse(json_data, mimetype='application/json')

def fetch_question(request):
  question_id = request.GET['question_id']
  question = Question.objects.get(id=question_id)
  profile = Profile.get_profile(request.user.student)
  tags = question.tags.all()
  answers = Answer.objects.filter(question=question).annotate(upvote_count=Count('upvoted_by')).order_by('-upvote_count')
  json_data = simplejson.dumps({'question':question_dict(question,profile),'answers':map(lambda a:answer_dict(a,profile), answers),
      'tags':map(lambda t:tag_dict(t,profile), tags)})
  return HttpResponse(json_data, mimetype='application/json')


def add_answer(request):
  question_id = request.POST['question_id']
  description = request.POST['description']
  question = Question.objects.get(id=question_id)
  profile = Profile.get_profile(request.user.student)
  answer = question.answer_set.create(description=description, profile=profile)
  json_data = simplejson.dumps({'answer':answer_dict(answer,profile)})
  return HttpResponse(json_data, mimetype='application/json')

def fetch_answer(request):
  answer_id = request.GET['answer_id']
  profile = Profile.get_profile(request.user.student)
  answer = Answer.objects.get(id=answer_id)
  question = answer.question
  json_data = simplejson.dumps({'answer':answer_dict(answer,profile),'question':question_dict(question,profile)})
  return HttpResponse(json_data, mimetype='application/json')

def follow_question(request):
  question_id = request.GET['question_id']
  question = Question.objects.get(id=question_id)
  profile = Profile.get_profile(request.user.student)
  if not ProfileQuestionFollowed.objects.filter(profile=profile,question=question).exists():
    ProfileQuestionFollowed.objects.create(profile=profile,question=question)
  return HttpResponse()

def unfollow_question(request):
  question_id = request.GET['question_id']
  question = Question.objects.get(id=question_id)
  profile = Profile.get_profile(request.user.student)
  if ProfileQuestionFollowed.objects.filter(profile=profile,question=question).exists():
    ProfileQuestionFollowed.objects.get(profile=profile,question=question).delete()
  return HttpResponse()

def remove_upvote(request):
  answer_id = request.GET['answer_id']
  answer = Answer.objects.get(id=answer_id)
  profile = Profile.get_profile(request.user.student)
  if ProfileAnswerFollowed.objects.filter(profile=profile,question=question).exists():
    ProfileAnswerUpvoted.objects.get(profile=profile,answer=answer).delete()
  count = len(ProfileAnswerUpvoted.objects.filter(answer=answer))
  json_data = simplejson.dumps({'count':count})
  return HttpResponse(json_data, mimetype='application/json')

def remove_downvote(request):
  answer_id = request.GET['answer_id']
  answer = Answer.objects.get(id=answer_id)
  profile = Profile.get_profile(request.user.student)
  if profile.answers_down.filter(id=answer.pk).exists():
   profile.answers_down.remove(answer)
  return HttpResponse()

def upvote_answer(request):
  answer_id = request.GET['answer_id']
  answer = Answer.objects.get(id=answer_id)
  profile = Profile.get_profile(request.user.student)
  if not ProfileAnswerUpvoted.objects.filter(profile=profile, answer=answer).exists():
    ProfileAnswerUpvoted.objects.create(profile=profile,answer=answer)
  if profile.answers_down.filter(id=answer_id).exists():
    profile.answers_down.remove(answer)
  count = len(ProfileAnswerUpvoted.objects.filter(answer=answer))
  json_data = simplejson.dumps({'count':count})
  return HttpResponse(json_data, mimetype='application/json')

def downvote_answer(request):
  answer_id = request.GET['answer_id']
  answer = Answer.objects.get(id=answer_id)
  profile = Profile.get_profile(request.user.student)
  if not profile.answers_down.filter(id=answer.pk).exists():
    profile.answers_down.add(answer)
  if ProfileAnswerUpvoted.objects.filter(profile=profile,answer=answer).exists():
    ProfileAnswerUpvoted.objects.get(profile=profile,answer=answer).delete()
  count = len(ProfileAnswerUpvoted.objects.filter(answer=answer))
  json_data = simplejson.dumps({'count':count})
  return HttpResponse(json_data, mimetype='application/json')

def fetch_tag(request):
  tag_name = request.GET['tag_name']
  profile = Profile.get_profile(request.user.student)
  tag = Tag.objects.get(name=tag_name)
  tag_item = TaggedItem.objects.filter(tag=tag,content_type=ContentType.objects.get_for_model(Question))
  questions = map(lambda t:tagitem_content(t,profile), tag_item)
  json_data = simplejson.dumps({'questions':map(lambda q:question_dict(q, profile), questions),'tag':tag_dict(tag,profile)})
  return HttpResponse(json_data, mimetype='application/json')

def fetch_activity(request):
  profile = Profile.get_profile(request.user.student)
  activities = Activity.objects.all()
  json_data = simplejson.dumps({'activities':map(lambda act:activity_dict(act, profile), activities)})
  return HttpResponse(json_data, mimetype='application/json')

def follow_tag(request):
  tag_name = request.GET['tag_name']
  profile = Profile.get_profile(request.user.student)
  tag = Tag.objects.get(name=tag_name)
  if not profile.tags_followed.filter(id=tag.id).exists():
    profile.tags_followed.add(tag)
    tag_item = TaggedItem.objects.get(tag=tag,content_type=ContentType.objects.get_for_model(Profile),object_id=profile.pk)
    Activity.objects.create(activity_type='FOL_TOPIC',content=tag_item)
  return HttpResponse()

def unfollow_tag(request):
  tag_name = request.GET['tag_name']
  profile = Profile.get_profile(request.user.student)
  tag = Tag.objects.get(name=tag_name)
  if profile.tags_followed.filter(id=tag.id).exists():
    tag_item = TaggedItem.objects.get(tag=tag,content_type=ContentType.objects.get_for_model(Profile),object_id=profile.pk)
    Activity.objects.get(activity_type='FOL_TOPIC',content_type=ContentType.objects.get_for_model(tag_item),object_id=tag_item.pk).delete()
    profile.tags_followed.remove(tag)
  return HttpResponse()

def search_tag(request):
  tag_key = request.POST['tag_key']
  tags = Tag.objects.filter(Q(name__icontains=tag_key))
  json_data = simplejson.dumps({'tags':map(tag_name,tags)})
  return HttpResponse(json_data, mimetype='application/json')

