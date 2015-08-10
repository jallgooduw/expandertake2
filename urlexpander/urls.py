from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.url_list, name='url_list'),
]
