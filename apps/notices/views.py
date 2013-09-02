# Create your views here
from django.contrib.auth.models import User
from django.shortcuts import render

def index(request):
  current_user = request.user
  context = {'user' : current_user}
  return render(request, 'notices/index.html', context)
  


