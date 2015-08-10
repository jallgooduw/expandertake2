from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.url_list, name='url_list'),
url(r'^post/(?P<pk>[0-9]+)/$', views.url_detail, name='url_detail'),
]
