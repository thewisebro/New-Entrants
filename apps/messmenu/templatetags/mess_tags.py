# python imports
from datetime import date, timedelta

# django imports
from django import template
from django.utils.html import strip_tags, escape
from django.utils.safestring import mark_safe

register = template.Library()


## returns date string '20/07' format when added no_of_days to date
@register.filter
def get_date_1(date, no_of_days):
  date += timedelta(days = no_of_days)
  date_str = date.strftime('%d/%m')
  return date_str


## returns date string '20 Jul' format when added no_of_days to date
@register.filter
def get_date_2(date, no_of_days):
  date += timedelta(days = no_of_days)
  date_str = date.strftime('%d')
  month_str = date.strftime('%b')
  if int(date_str) < 10:
    date_str = date_str[1]
  date_str = date_str + ' ' + month_str
  return date_str


@register.filter
def get_date_1_week(date, weeks):
  date += timedelta(days = weeks * 7)
  return date


@register.filter
def easy_escape(text):
  text = escape(text)
  text = text.replace('\r\n', '<br/>')
  text = text.replace('\n', '<br/>')
  ## allow spaces
  text = text.replace('  ', ' &nbsp;')
  text = mark_safe(text)
  return text

