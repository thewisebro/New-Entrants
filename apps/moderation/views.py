import json

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from api.utils import dialog_login_required, ajax_login_required
from moderation.models import Report, Reportable
from moderation.forms import ReportForm, REPORT_CHOICES

@dialog_login_required
def submit_report(request):
  content_type_pk = request.GET['content_type_pk']
  object_pk = request.GET['object_pk']
  close = False
  try:
    content_type = ContentType.objects.get(pk=content_type_pk)
    model = content_type.model_class()
    assert issubclass(model, Reportable)
    content = model.objects.get(pk=object_pk)
  except:
    close = True
  if Report.objects.filter(content_type=content_type,
      object_id=object_pk, reported_by=request.user).exists():
    close = True
    messages.info(request, "You've already reported this item.")
  form = ReportForm()
  if request.method == 'POST':
    form = ReportForm(request.POST)
    if form.is_valid():
      reason = form.cleaned_data['reason']
      description = dict(REPORT_CHOICES)[reason]
      report = Report.objects.create(
          reported_by=request.user,
          description=description,
          content_type=content_type,
          object_id=object_pk
      )
      messages.info(request, "Thank you for reporting.")
      if request.user.in_group('IMG Member'):
        report.flagged = True
        report.moderated_by = request.user
        report.save()
        content.trash()
        messages.success(request, "Item has been trashed.")
      elif Report.objects.filter(content_type=content_type,
              object_id=object_pk).count() >= 7:
        Report.objects.filter(content_type=content_type,
              object_id=object_pk).update(flagged=True)
        content.trash()
      close = True
  if close:
    return HttpResponseRedirect(reverse('close_dialog', kwargs={
          'dialog_name': 'report_dialog'
    }))
  return render(request, 'moderation/dialogs/submit_report.html', {
    'form': form
  })

@ajax_login_required
def report_info(request):
  content_type_pk = request.GET['content_type_pk']
  object_pk = request.GET['object_pk']
  open_dialog = True
  try:
    content_type = ContentType.objects.get(pk=content_type_pk)
    model = content_type.model_class()
    assert issubclass(model, Reportable)
    content = model.objects.get(pk=object_pk)
  except:
    open_dialog = False
  if Report.objects.filter(content_type=content_type,
      object_id=object_pk, reported_by=request.user).exists():
    open_dialog = False
    messages.info(request, "You've already reported this item.")
  json_data = json.dumps({
    'open_dialog': open_dialog,
  })
  return HttpResponse(json_data, content_type='application/json')
