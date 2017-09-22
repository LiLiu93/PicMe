# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.DialogListView.as_view(),
        name='dialogs_detail'
    ),
    url(
        regex=r'^$',
        view=views.DialogListView.as_view(),
        name='dialogs'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/read/$',
        view=views.set_read_message,
        name='set_read_message'
    ),
    url(
        regex=r'^unread/message/$',
        view=views.unread_message,
        name='unread_message'
    ),
]
