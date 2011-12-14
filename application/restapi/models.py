from django.db import models               
from django.core.cache import cache
import sqlite3


# Create your models here.

class StationManager(models.Manager):  
    def get_station(self,code):
      try:
        station = cache.get('station_'+code,'')
        if not station:
          station = self.get(code=code)
          cache.set('station_'+code,station)
      
        data = {'name':station.name.upper(), 'code':station.code.upper()}
      except:
        data = {'name':code.upper(),'code':code.upper()}
      
      return data
    
class Station(models.Model):
  code = models.CharField(max_length=10,primary_key=True)
  name = models.CharField(max_length=100)
  objects = StationManager()


class Schedule():
  def get_departure_time(self, train_number, station_code):
    try :
      conn = sqlite3.connect('/data/indian_railways.sqlite3')
      query = 'select departure from schedule where train_number=%s and station_code="%s"' % (train_number, station_code )
      c = conn.cursor()
      c.execute(query)
      row = c.fetchone()
      return row[0]
    except:
      return '';

  def get_arrival_time(self, train_number, station_code):
    try :
      conn = sqlite3.connect('/data/indian_railways.sqlite3')
      query = 'select arrival from schedule where train_number=%s and station_code="%s"' % (train_number, station_code )
      c = conn.cursor()
      c.execute(query)
      row = c.fetchone()
      return row[0]
    except:
      return '';
