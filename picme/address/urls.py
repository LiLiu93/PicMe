from . import views

from django.conf.urls import url


app_name = 'address'

urlpatterns = [
    url(r'^getCityList/$', views.getCityList, name='getCityList'),
]