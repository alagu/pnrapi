import os
import sys

sys.path.append('/srv/www/pnrapi.alagu.net/application')
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)),'..'))


os.environ['PYTHON_EGG_CACHE'] = '/srv/www/pnrapi.alagu.net/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import newrelic.agent
newrelic.agent.initialize('/srv/www/pnrapi.alagu.net/application/newrelic.ini')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
application = newrelic.agent.wsgi_application()(application)
