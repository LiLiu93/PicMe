from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.db.models import Q
from .forms import PostForm, EditPostForm
from django.contrib.auth.models import User
from .models import Post, Comment
from address.models import State, City
from django.views.decorators.csrf import ensure_csrf_cookie
from base64 import b64decode
from django.core.files.base import ContentFile

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden

from django.core import serializers
import re

import json
import logging
import geoip2.database

logger = logging.getLogger(__name__)


@login_required
def new_post(request):

	if request.method == 'POST':
		current_user = request.user
		form = PostForm(request.POST, request.FILES or None, instance=Post(user=current_user))

		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.file_type = request.FILES.get('post_picture').content_type.split('/')[0]
			post.save()
			return HttpResponseRedirect('/posts/'+str(post.id)+"/")
		else:
			form = PostForm(request.POST)
			dict_list = {
				'user': request.user,
				'form': form,
				'message': 'New post created successfully'
			}
			return render(request, 'posts/new.html', dict_list)
	else:
		form = PostForm()
		dict_list = {
			'user': request.user,
			'form': form,
			'message': 'New post created successfully'
		}
		return render(request, 'posts/new.html', dict_list)


# class IndexView(ListView):
# 	template_name = 'posts/index.html'
# 	context_object_name = 'posts'

# 	@method_decorator(login_required)
# 	def dispatch(self, request, *args, **kwargs):
# 		return super(ListView, self).dispatch(request, *args, **kwargs)

# 	def get_queryset(self):
# 		return Post.objects.filter(show=True).order_by('-created')


@login_required
def show_post_list(request):
	posts = Post.objects.filter(show=True).order_by('-created')

	current_user = request.user

	like_posts = current_user.likes_posts.all()

	ip = request.META['REMOTE_ADDR']
	# ip = '71.60.32.90'
	reader = geoip2.database.Reader('address/GeoLite2-City.mmdb')
	response = reader.city(ip)
	city = (str(response.city.name)).upper()
	try:
		posts_nearby = Post.objects.filter(show=True, post_city=City.objects.get(name=city)).order_by('-numberOfLikes')[:3]
	except City.DoesNotExist:
		posts_nearby = None
	context = {
		'posts': posts,
		'like_posts': like_posts,
		'posts_nearby': posts_nearby,
	}

	reader.close()

	return render(request, 'posts/index.html', context)



@login_required
def show_post_list_by_pop(request):
	posts = Post.objects.filter(show=True).order_by('-numberOfLikes')

	current_user = request.user

	like_posts = current_user.likes_posts.all()

	context = {
		'posts': posts,
		'like_posts': like_posts,
	}

	return render(request, 'posts/index.html', context)

@login_required
def show_post_list_by_Comment(request):
	posts = Post.objects.filter(show=True).order_by('-numberOfComment')

	current_user = request.user

	like_posts = current_user.likes_posts.all()

	context = {
		'posts': posts,
		'like_posts': like_posts,
	}

	return render(request, 'posts/index.html', context)


@login_required
def post_detail(request, post_id):

	post = get_object_or_404(Post, id=post_id)

	if not post.show:
		raise Http404('Post does not exist')

	context = {'post': post}

	return render(request, 'posts/detail.html', context)


# List all of the Posts of the user
class UserPostListView(ListView):
	template_name = 'posts/userposts.html'
	context_object_name = 'posts'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ListView, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return Post.objects.filter(
			Q(user=self.request.user.user_profile) &
			Q(show=True))


@login_required
def delete_post(request, post_id):

	if request.method == 'GET':
		raise Http404('Can\'t delete post using GET method')

	message = ''

	logging.debug("[post_id] = " + str(post_id))

	if request.method == 'POST':

		post = get_object_or_404(Post, id=post_id)

		post_user = post.user
		current_user = request.user

		if not post.show:
			raise Http404('Post does not exist')

		if post_user == current_user:
			post = Post.objects.get(id=post_id)
			post.show = False
			post.save()
			message = 'Delete Successfully'
		else:
			message = 'The post does not belong to you'

	posts = Post.objects.filter(show=True)
	context = {
		'posts': posts,
		'user': request.user,
		'message': message
	}

	return render(request, 'posts/index.html', context)


@login_required
def like_post(request, post_id):

	current_user = request.user
	posts = Post.objects.filter(show=True)
	post = Post.objects.get(id=post_id)

	if not post.show:
		raise Http404('Post does not exist')

	context = {
		'user': current_user,
		'posts': posts
	}

	if current_user in post.likes.all():
		post.likes.remove(current_user)
		post.numberOfLikes = post.numberOfLikes - 1
		post.save()
	else:
		post.likes.add(current_user)
		post.numberOfLikes = post.numberOfLikes + 1
		post.save()

	return render(request, 'posts/index.html', context)


@login_required
def search_by_location(request):
	try:
		key = request.GET.get('key')
	except:
		key = ''
	if key != '':

		try:
			state_keys = State.objects.filter(name__icontains=key)
		except State.DoesNotExist:
			state_keys = []

		try:
			city_keys = City.objects.filter(name__icontains=key)
		except City.DoesNotExist:
			city_keys = []

		try:
			post_list = Post.objects.filter(
				(Q(post_state__in=state_keys) |
				Q(post_city__in=city_keys)) &
				Q(show=True)
			).order_by('-created')
		except Post.DoesNotExist:
			post_list = []

	else:
		post_list = Post.objects.filter(show=True).order_by('-created')

	context = {
		'user': request.user,
		'posts': post_list
	}
	return render(request, 'posts/index.html', context)


@login_required
def get_post_photo(request, post_id):
	post = Post.objects.get(id=post_id)

	if not post.show:
		raise Http404('Post does not exist')

	return HttpResponse(post.post_picture, content_type=post.content_type)


@login_required
def recover_post(request, post_id):

	if not request.method == 'POST':
		raise Http404('Can not recover post using GET method')
	else:
		post = get_object_or_404(Post, id=post_id)
		if not post.user == request.user:
			message = 'The post does not belong to you'
			return render(request, 'posts/error_page.html', {'message': message})
		if post.show:
			message = 'Can not recover an existed post'
			return render(request, 'posts/error_page.html', {'message': message})

		post.show = True
		post.save()

		context = {
			'posts': Post.objects.filter(show=True).order_by('-created'),
			'user': request.user,
			'message': 'Recover post successfully'
		}

		return render(request, 'posts/index.html', context)


@login_required
def follow_posts(request):

	current_user = request.user
	user_profile = current_user.user_profile
	followers = user_profile.follows.all()

	follow_posts = []

	for follower in followers:
		posts = Post.objects.filter(
			Q(user=follower) &
			Q(show=True)
			)
		follow_posts.extend(posts)

	follow_posts.sort(key=lambda r: r.created, reverse=True)

	like_posts = current_user.likes_posts.all()

	context = {
		'posts': follow_posts,
		'like_posts': like_posts,
	}

	return render(request, 'posts/follow_posts.html', context)


@login_required
def get_post_list_by_location(request, username):
	user = User.objects.get(username=username)
	posts = Post.objects.filter(user=user, show=True)

	post_dic = {}
	json_list = list()

	for post in posts:
		city = post.post_city
		loc_post = post_dic.get(city)

		if loc_post is None:
			post_dic[city] = [post]
		else:
			post_dic[city].append(post)

		for city, post_list in post_dic.items():
			json_list.append(([city.name], [city.state], [city.latitude], [city.longitude], [len(post_list)]))

	return HttpResponse(json.dumps(json_list), content_type='application/json')


def get_all_posts_for_map(request):
	posts = Post.objects.filter(show=True)

	post_dic = {}
	json_list = list()

	for post in posts:
		city = post.post_city
		loc_post = post_dic.get(city)

		if loc_post is None:
			post_dic[city] = [post]
		else:
			post_dic[city].append(post)

		for city, post_list in post_dic.items():
			json_list.append(([city.name], [city.state], [city.latitude], [city.longitude], [len(post_list)]))

	return HttpResponse(json.dumps(json_list), content_type='application/json')


@login_required
def get_comments(request, post_id):
	post = Post.objects.get(id = post_id)
	comments = Comment.objects.filter(belong_post = post)
	response_text = construct_json(request, comments)
	return HttpResponse(response_text, content_type='application/json')

@login_required
def add_comments(request, post_id):
	if request.POST['content'] and not re.match('^\s*$', request.POST['content']):
		post = Post.objects.get(id=post_id)
		comment = Comment(content = request.POST['content'], sender = request.user, belong_post = post)
		comment.save()
		comments = Comment.objects.filter(id = comment.id)
		post.numberOfComment = post.numberOfComment + 1
		post.save()

		response_text = construct_json(request, comments)
		return HttpResponse(response_text, content_type='application/json')

def construct_json(request,items):
	r = '['
	for item in items:
		r = r + '{"pk": ' + str(item.id) + ', '
		r = r + '"content": "' + item.content + '", '
		r = r + '"time": "' + str(item.created)[0:len(str(item.created))-13] + '", '
		r = r + '"name": "' + item.sender.username + '"}, '
	if (len(items) != 0):
		r = r[0:len(r) - 2]
	r = r + ']'
	return r

#@login_required
#def comments(request, post_id):
#	post = Post.objects.get(id=post_id)
#
#	if request.method == 'GET':
#		context = {
#			'post': post
#		}
#
#		return render(request, 'posts/comment.html', context)

@login_required
def goto_photo_editor(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		if post.user != request.user or post.file_type == 'video':
			return HttpResponseForbidden()
		if post.show == False:
			return HttpResponseForbidden()
		else:
			context = {'post':post}
			return render(request, 'posts/edit_photo.html', context)
	except Post.DoesNotExist:
		raise Http404


@login_required
def goto_editor(request, post_id):
	try:
		post = Post.objects.select_for_update().get(id=post_id)
		if post.user != request.user:
			return HttpResponseForbidden()
		if post.show == False:
			return HttpResponseForbidden()
		if request.method == 'GET':
			form = EditPostForm(instance=post, city=post.post_city)
			context = { 'post': post, 'form': form}
			return render(request, 'posts/edit.html', context)

		form = EditPostForm(request.POST, instance=post)

		if not form.is_valid():
			form = EditPostForm(request.POST, instance=post, city=post.post_city)
			context = { 'post': post, 'form': form,'message':"Not saved"}
			return render(request, 'posts/edit.html', context)
		else:
			post.save()
			form.save()

		context = { 'post': post}
		return render(request, 'posts/detail.html', context)
	except Post.DoesNotExist:
		raise Http404




@login_required
def update_photo(request, post_id):
	try:
		post = Post.objects.get(id=post_id)

		if post.user != request.user:
			return HttpResponseForbidden()
		if post.show == False:
			return HttpResponseForbidden()

		if request.POST['image']:
			image_64 = request.POST['image']
			image_64 = image_64.replace("data:image/png;base64,", "")
			image_64 = image_64.replace(" ", "+")
			image_data = b64decode(image_64)

			name = 'decode'+str(post_id)+'.png'
			post.post_picture= ContentFile(image_data, name)
			# post.post_picture.save(image_result)
			post.save()
		context = {'post': post}

		return render(request, 'posts/edit.html', context)
	except Post.DoesNotExist:
		raise Http404

