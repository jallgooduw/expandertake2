from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf.urls import include

urlpatterns = [
    url(r'^$', views.url_list, name='url_list'),
    url(r'^url/(?P<pk>[0-9]+)/$', views.url_detail, name='url_detail'),
    url(r'^url/new/$', views.url_new, name='url_new'),
    url(r'^url/(?P<pk>[0-9]+)/remove/$', views.url_remove, name='url_remove'),
    url(r'^api/(?P<pk>[0-9]+)/$', views.url_apidetail, name='url_apidetail'),
    url(r'^api/$', views.url_apilist, name='url_apilist'),
    #url(r'^books/$', views.book_list),

]



urlpatterns = format_suffix_patterns(urlpatterns)

