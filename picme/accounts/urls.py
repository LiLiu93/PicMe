from . import views

from django.conf.urls import url

from posts import views as posts_views

app_name = 'accounts'

urlpatterns = [

	# Follow another user
	url(r'^follow/$', views.follow, name='follow'),

	# UnFollow another user
	url(r'^unfollow/$', views.unfollow, name='unfollow'),

	# override this url in userena
	url(r'^$', views.toIndex, name='toIndex'),
]