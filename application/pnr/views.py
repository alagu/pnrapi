# Create your views here.
from django.http import HttpResponse, Http404
import datetime
import httplib, urllib
import re
import os
import time
import logging
import copy
from django.utils import simplejson as json
from django.core.cache import cache
import models

TWO_WEEKS    = 1209600
HALF_DAY     = 43200
PNR_CACHE_KEY = "pnr:%s"

def index(request):
  return HttpResponse('hi')


def query(request, pnr_num):
  jsonp = request.GET['jsonp'] if 'jsonp' in request.GET else None
  cache_key = PNR_CACHE_KEY % (pnr_num)

  return_object = cache.get(cache_key)
  
  if not return_object:
    return_object = models.curl_indian_railways(pnr_num)
    cur_time = int(time.time())
    if return_object['status'] == 'OK':
        travel_ts = return_object['data']['travel_date']['timestamp']
        if (int(travel_ts) - cur_time) > TWO_WEEKS:
            print (int(travel_ts)-cur_time)
            print return_object
            cache.set(cache_key,return_object)
    
  data = json.dumps(return_object)
  if jsonp:
    data = jsonp + '(' + data + ')'

  response = HttpResponse(data)
  
  return response
