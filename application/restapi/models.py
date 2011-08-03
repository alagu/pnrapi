from django.db import models               
from django.core.cache import cache

# Create your models here.
class Station(models.Model):
    code = models.TextField()
    name = models.TextField()
    
def get_station(code):
  try:
    station = Station.objects.get(code=code)
    data = {'name':station.name, 'code' : station.code.upper()}
  except: #DoesNotExist
    data = {}

  return data
