from django.shortcuts import render

def header(request):
  return render(request, 'nucleus/pagelets/header.html')
