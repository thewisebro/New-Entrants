# python imports
import threading, random

# django imports
from django.shortcuts import render_to_response
from django.conf import settings
from django.template.context import RequestContext

# local imports
from messmenu.utils.food_facts import food_facts


def response_adapter(params_dict):
  currentThread = threading.currentThread()
  request = currentThread.request

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
    'images_url': static_url + 'images/messmenu',
    'styles_url': static_url + 'css/messmenu',
    'scripts_url': static_url + 'js/messmenu',
  }
  params_dict.update(fixed_params)
  return render_to_response(params_dict['content'],
                            params_dict,
                            context_instance = RequestContext(request))
