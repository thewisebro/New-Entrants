import re

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template import RequestContext 
from django.db.models import Q

from facapp.models import *
from facapp.utils import handle_exc
from facapp.forms import BooksAuthoredForm, RefereedJournalPapersForm, PhotoUploadForm, ResumeUploadForm
from core.forms import BaseForm, BaseModelForm # , BaseModelFormFunction, ConfirmDeleteForm

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
def books_authored_edit(request):
  try:
    faculty = request.user.faculty
    # Get the previous entry or null entry if there isn't one. Here we are not guaranteed 
    # that there will be an entry in the table. So we need to check.
    old = BooksAuthored.objects.filter(faculty=faculty)
    if len(old) == 0:
      old = None
    else:
      old = old[0]
    if request.method == 'POST':
      books_authored_form = BooksAuthoredForm(data=request.POST)
      if books_authored_form.is_valid():
        new_entry = books_authored_form.save(commit=False)
        new_entry.faculty = faculty
        new_entry.save()
        messages.success(request, 'Books Authored information was successfully updated')
        # Update old object and send it to the view page.
        old = BooksAuthored.objects.filter(faculty=faculty)[0]
        return render(request, 'facapp/books_authored.html', {
            'content': old,
            })
      else:
        messages.error(request, 'Invalid data in form submission')
        return HttpResponseRedirect(reverse('facapp.views.index'))
    # Fill the form with the instance in DB and send it to edit template.
    books_authored_form = BooksAuthoredForm(instance=old)
    return render(request, 'facapp/books_authored_edit.html', {
        'form': books_authored_form,
        'action':'/facapp/books_authored/edit/',
        })
  except Exception as e:
    handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
def refereed_journal_papers_edit(request):
  '''  This view function is similar to books_authored_edit view function.  '''
  try:
    faculty = request.user.faculty
    old = RefereedJournalPapers.objects.filter(faculty=faculty)
    if len(old) == 0:
      old = None
    else:
      old = old[0]

    if request.method == 'POST':
      rjp_form = RefereedJournalPapersForm(request.POST)
      if rjp_form.is_valid():
        new_entry = rjp_form.save(commit=False)
        new_entry.faculty = faculty
        new_entry.save()
        messages.success(request, 'Refereed Journal Papers information was successfully updated')
        old = RefereedJournalPapers.objects.filter(faculty=faculty)[0]
        return render(request, 'facapp/refereed_journal_papers.html', {
            'content': old,
            })
      else:
        messages.error(request, 'Invalid data in form submission')
        return HttpResponseRedirect(reverse('facapp.views.index'))

    rjp_form = RefereedJournalPapersForm(instance=old)
    return render(request, 'facapp/refereed_journal_papers_edit.html', {
        'form': rjp_form,
        'action':'/facapp/refereed_journal_papers/edit/',
        })
  except Exception as e:
    handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
def books_authored(request):
  # import ipdb; ipdb.set_trace()
  try:
    faculty = request.user.faculty
    old = BooksAuthored.objects.filter(faculty=faculty)
    if len(old) == 0:
      old = None
    else:
      old = old[0]
    return render(request, 'facapp/books_authored.html', {
        'content': old,
        })
  except Exception as e:
    handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
def refereed_journal_papers(request):
  try:
    faculty = request.user.faculty
    old = RefereedJournalPapers.objects.filter(faculty=faculty)
    if len(old) == 0:
      old = None
    else:
      old = old[0]
    return render(request, 'facapp/refereed_journal_papers.html', {
        'content': old,
        })
  except Exception as e:
    handle_exc(e, request)

