from . import views

from django.conf.urls import url

app_name = 'posts'

urlpatterns = [
	url(r'^$', views.show_post_list, name='index'),

	url(r'^list_by_pop/?$', views.show_post_list_by_pop, name='pop'),

	url(r'^list_by_comment/?$', views.show_post_list_by_Comment, name='comment'),

	url(r'^search/?$', views.search_by_location, name='search'),

	url(r'^new/?$', views.new_post, name='new'),

	url(r'^user_posts/?$', views.UserPostListView.as_view(), name="user_posts"),

	url(r'^(?P<post_id>[0-9]+)/?$', views.post_detail, name='detail'),

	url(r'^delete_post/(?P<post_id>[0-9]+)/?$', views.delete_post, name='delete_post'),

	url(r'^like_post/(?P<post_id>[0-9]+)/?$', views.like_post, name='like_post'),

	url(r'^post_photo/(?P<post_id>[0-9]+)/?$', views.get_post_photo, name='get_post_photo'),

	url(r'^recover_post/(?P<post_id>[0-9]+)/?$', views.recover_post, name='recover_post'),

	url(r'^follow_posts/?$', views.follow_posts, name='follow_posts'),

	url(r'^loc_post/(?P<username>\w+)/?$', views.get_post_list_by_location, name='post_by_location'),

	# get all posts, and pack into json
	url(r'^all_posts_for_map/?$', views.get_all_posts_for_map, name='all_post_for_map'),

	url(r'^get_comment/(?P<post_id>[0-9]+)/?$', views.get_comments, name='getcomment'),

	url(r'^add_comment/(?P<post_id>[0-9]+)/?$', views.add_comments, name='addcomment'),

	url(r'^edit/(?P<post_id>[0-9]+)/?$', views.goto_editor, name='editor'),

	url(r'^edit_photo/(?P<post_id>[0-9]+)/?$', views.goto_photo_editor, name='photo_editor'),

	url(r'^update_photo/(?P<post_id>[0-9]+)/?$', views.update_photo, name='update_photo'),

]
