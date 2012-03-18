from django.conf.urls.defaults import *

urlpatterns = patterns('house.views',
    url(r'^klub/(?P<pk>\d+)/$', 'klub', name='house_klub'),
    url(r'^posel/(?P<slug>[^/]*)/$', 'posel', name='house_posel'),
    url(r'^posiedzenie/(?P<pk>\d+)/$', 'posiedzenie', name='house_posiedzenie'),
    url(r'^punkt/(?P<pk>\d+)/$', 'punkt', name='house_punkt'),
    url(r'^glosowanie/(?P<pk>\d+)/$', 'glosowanie', name='house_glosowanie'),
)
