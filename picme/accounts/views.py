from django.shortcuts import render,reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

import logging
logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def follow(request):
	logging.debug("[followId] = " + "Herere")
	if request.method == 'POST':
		followId = request.POST.get('followId')

		user = request.user
		user.user_profile.follows.add(followId)
		user.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def unfollow(request):
	if request.method == 'POST':
		unfollowId = request.POST.get('unfollowId')
		logging.debug('[unfollowId] = ' + unfollowId )
		unfollowUser = get_object_or_404(User,id = unfollowId)
		user = request.user
		user.user_profile.follows.remove(unfollowUser)
		user.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def toIndex(request):
	return redirect('posts:index')