from django.core.cache import cache
import sqlite3


class Station():
  def get_station(self,code):
    try:
      station = cache.get('station_'+code,'')
      if not station:
        print "Not cache"
        conn = sqlite3.connect('data/indian_railways.sqlite3')
        query = 'select name from stations where code="%s"' % (code)
        c = conn.cursor()
        c.execute(query)
        row = c.fetchone()
        station = row[0]
        cache.set('station_' + code, station)
      
      data = {'name':station.upper(), 'code':code.upper()}
    except :

      data = {'name':code.upper(), 'code':code.upper()}

    return data


class Schedule():
  def get_departure_time(self, train_number, station_code):
    try :
      conn = sqlite3.connect('data/indian_railways.sqlite3')
      query = 'select departure from schedule where train_number=%s and station_code="%s"' % (train_number, station_code )
      c = conn.cursor()
      c.execute(query)
      row = c.fetchone()
      return row[0]
    except:
      return '';

  def get_arrival_time(self, train_number, station_code):
    try :
      conn = sqlite3.connect('data/indian_railways.sqlite3')
      query = 'select arrival from schedule where train_number=%s and station_code="%s"' % (train_number, station_code )
      c = conn.cursor()
      c.execute(query)
      row = c.fetchone()
      return row[0]
    except:
      return '';
