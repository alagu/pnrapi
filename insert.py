import json
import _mysql
data = json.loads(open('railways_code.json').read())
db=_mysql.connect("127.0.0.1","root","allagappan","pnrapi")
for station in data['data']:
  sql = 'INSERT INTO restapi_station (`code`,`name`) values("%s","%s")' % (station['code'], station['name'])
  try :
    db.query(sql)
    print station['name'] + ' inserted ' 
  except :
    print '%s already inserted' % (sql)
