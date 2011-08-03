from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('pnr.views',
    (r'^$', 'index'),
   	(r'^(?P<pnr_num>\d+)', 'query')
)
