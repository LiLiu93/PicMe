from . import views

from django.conf.urls import include, url


app_name = 'base'


urlpatterns = [
    url(r'^test/$', views.test, name='test'),
]