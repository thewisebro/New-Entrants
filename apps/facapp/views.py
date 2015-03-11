import re

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template import RequestContext 
from django.db.models import Q

from nucleus.models import Branch
from facapp.models import *
from facapp.utils import handle_exc
# from facapp.forms import BooksAuthoredForm, RefereedJournalPapersForm, PhotoUploadForm, ResumeUploadForm
from api.forms import BaseForm, BaseModelForm, BaseModelFormFunction, ConfirmDeleteForm
# import pika
from django.utils import simplejson

# Create your views here.
