# python imports
import random
import threading

# django imports
from django.shortcuts import render_to_response
from django.conf import settings
from django.template.context import RequestContext

# local imports
from messmenu.utils.food_facts import food_facts


def add_common_functionality(request):

  static_url = settings.STATIC_URL
  len_facts = len(food_facts)
  fact = food_facts[random.randint(0, len_facts - 1)]
  food_fact = {
    'head': fact[0],
    'body': fact[1],
  }

  fixed_params = {
    'food_fact': food_fact,
    'is_mess_secy': request.user.groups.filter(name = 'Mess Secy').exists(),
    'IMAGES_URL': static_url + 'images/messmenu/',
    'CSS_URL': static_url + 'css/messmenu/',
    'JS_URL': static_url + 'js/messmenu/',
  }
  return fixed_params
