from django.conf.urls.defaults import patterns, include, url
import pnr

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pnrapi.views.home', name='home'),
    # url(r'^pnrapi/', include('pnrapi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
  	(r'^api/v1.0/pnr/', include('pnr.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
  	(r'^api/v1.0/', include('restapi.urls')),
)
