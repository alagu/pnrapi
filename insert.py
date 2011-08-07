import json
import _mysql
data = json.loads(open('railways_code.json').read())
db=_mysql.connect("127.0.0.1","root","root","pnrapi")
for station in data['data']:
  sql = 'INSERT INTO restapi_station (`code`,`name`) values("%s","%s")' % (station['code'], station['name'])
  try :
    sql
    db.query(sql)
  except :
    print '%s already inserted' % (sql)
