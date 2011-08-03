from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('restapi.views',
    (r'^station/(?P<station_code>\w+)$', 'station'),
)
