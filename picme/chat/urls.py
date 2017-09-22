from . import views

from django.conf.urls import url

app_name = 'chat'

urlpatterns = [
	url(r'^(?P<receiver_id>[0-9]+)/$', views.make_room, name="make_room"),
	url(r'^(?P<receiver_id>[0-9]+)/new_messages/$', views.message_not_view, name="message_not_view"),
	url(r'^(?P<receiver_id>[0-9]+)/read/$', views.read_message, name="read_message"),
	url(r'^(?P<receiver_id>[0-9]+)/send/$', views.send_message, name="send_message"),

	url(r'^unread/$', views.unread_message, name="unread_message"),

]
