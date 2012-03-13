from django.conf.urls.defaults import *

urlpatterns = patterns('house.views',
    url(r'^k/(?P<pk>\d+)/$', 'klub', name='house_klub'),
    url(r'^ps/(?P<slug>[^/]*)/$', 'posel', name='house_posel'),
    url(r'^pd/(?P<pk>\d+)/$', 'posiedzenie', name='house_posiedzenie'),
    url(r'^pk/(?P<pk>\d+)/$', 'punkt', name='house_punkt'),
    url(r'^g/(?P<pk>\d+)/$', 'glosowanie', name='house_glosowanie'),
)
