from django.conf.urls.defaults import *

urlpatterns = patterns('people.views',
    url(r'^uzytkownik/$', 'settings', name='people_settings'),
    url(r'^uzytkownik/(?P<username>[^/]*)/$', 'user', name='people_user'),
    url(r'^ufaj/(?P<username>[^/]*)/$', 'follow', name='people_follow'),
    url(r'^odufaj/(?P<username>[^/]*)/$', 'unfollow', name='people_unfollow'),
    url(r'^glosuj/(?P<pk>\d+)/$', 'vote', name='people_vote'),
    url(r'^odglosuj/(?P<pk>\d+)/$', 'unvote', name='people_unvote'),
    url(r'^poslowie/', 'rank', name='people_ranking'),
)
