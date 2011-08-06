from django.db import models               
from django.core.cache import cache

# Create your models here.

class StationManager(models.Manager):	
    def get_station(self,code):
		try:
			station = cache.get('station_'+code,'')
			cached = True
			if not station:
				cached = False
				station = self.get(code=code)
				cache.set('station_'+code,station)
			
			data = {'name':station.name.upper(), 'code':station.code.upper(),'cache':cached}
		except:
			data = {'name':code.upper(),'code':code.upper()}
			
		return data
		
class Station(models.Model):
	code = models.CharField(max_length=10,primary_key=True)
	name = models.CharField(max_length=100)
	objects = StationManager()