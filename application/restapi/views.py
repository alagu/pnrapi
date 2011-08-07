# Create your views here.
from django.http import HttpResponse, Http404
from django.utils import simplejson as json
from django.shortcuts import render_to_response


import models

def station(request, station_code):
  station_code = station_code.lower()
  data = models.Station.objects.get_station(code=station_code)
  status = 'OK'
  
  return_obj = {'status' : status, 'data' : data}
  response = HttpResponse(json.dumps(return_obj))
  response['Content-Type'] = 'text/plain'
  return response

def index(request):
  return render_to_response('index.html')
