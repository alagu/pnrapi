from django.db import models
import datetime
import httplib, urllib
import re
import os
import time
import logging
import restapi

# Create your models here.

def curl_indian_railways(pnr_num):
  return_object = {}
  lccp_pnrno1 = pnr_num[:3]
  lccp_pnrno2 = pnr_num[3:]
  params = urllib.urlencode({'lccp_pnrno1': lccp_pnrno1, 'lccp_pnrno2': lccp_pnrno2, 'submitpnr': 'Get Status'})
  headers = {"Content-type": "application/x-www-form-urlencoded",
             "Host": "www.indianrail.gov.in",
             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
             "Accept-Language": "en-us,en;q=0.5",
             "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
             "Keep-Alive": "115",
             "Connection": "keep-alive",
             "Referer": "http://www.indianrail.gov.in/pnr_stat.html",
             "Accept": "text/plain"}
  host = 'www.indianrail.gov.in'
  path = '/cgi_bin/inet_pnrstat_cgi.cgi'
  conn = httplib.HTTPConnection(host,80,timeout=10)
  return_object = {}
  return_object['status'] = 'OK'
  return_object['data']   = {}

  try :
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    
    contents = data.split('\n')
    
    statuslines = []
    for line in contents:
      if line.find('border_both') != -1 and line.find('TD') != -1:
        statuslines.append(line)

    if len(statuslines) == 0:
      return_object['status'] = 'INVALID'
      return_object['data']   = {'pnr_number' : pnr_num , 'message' : 'Invalid number'}

    expression = re.compile('>(.*)<')

    i = 0
    passenger_count = 0
    passenger_line  = -1
    chart_prepared = True
    for line in statuslines:
       matches = expression.findall(line) 
       if len(matches) > 0 :
          statement =  matches[0].replace('<B>','').replace('</B>','')
          statement = statement.strip()
          #print statement

          if(i == 0):
            return_object['data']['train_number'] = statement.replace('*','')
          elif(i==1):
            return_object['data']['train_name'] = statement
          elif(i==2):
            date = statement.replace(' ','')
            timeobj = time.strptime(date, "%d-%m-%Y")
            return_object['data']['travel_date'] = {'timestamp':int(time.mktime(timeobj)),'date':date}
          elif(i==3):
            return_object['data']['from'] = restapi.models.Station.objects.get_station(code=statement)
          elif(i==4):
            return_object['data']['to'] = restapi.models.Station.objects.get_station(code=statement)
          elif(i==5):
            return_object['data']['alight'] = restapi.models.Station.objects.get_station(code=statement)
          elif(i==6):
            return_object['data']['board'] = restapi.models.Station.objects.get_station(code=statement)
          elif(i==7):
            return_object['data']['class'] = statement
          elif(i>7):
            if statement.find('Passenger') != -1:
              passenger_count = passenger_count + 1
              passenger_line = 0
              if (passenger_count == 1):
                return_object['data']['passenger'] = [] 
              return_object['data']['passenger'].append({'seat_number':'','status':''})
              continue
            else:
              if passenger_line == 0:
                return_object['data']['passenger'][passenger_count-1]['seat_number'] = re.sub(r'\s', '',statement)
                passenger_line = passenger_line + 1
              elif passenger_line == 1:
                return_object['data']['passenger'][passenger_count-1]['status'] = re.sub(r'\s', '',statement)
                passenger_line = passenger_line + 1
            
            if i>7 and statement.find('CHART NOT PREPARED'):
              chart_prepared = False
          i=i+1
          
    return_object['data']['chart_prepared'] = chart_prepared
    return_object['data']['pnr_number'] = pnr_num
  except Exception as inst:
    return_object['status'] = 'TIMEOUT'
    return_object['data']   = {'pnr_number' : pnr_num , 'message' : 'Request Timed Out'}
    logging.debug('TIMEOUT ' + pnr_num)
    
  
  return return_object
