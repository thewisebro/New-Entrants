from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
  return render(request, 'nucleus/index.html')

def close_dialog(request, dialog_name):
  return render(request, 'close_dialog.html', {'dialog_name': dialog_name})
