from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Message
from django.contrib.auth.models import User
from django.http import Http404
import json


def make_room(request, receiver_id):
	user_visited = get_object_or_404(User, id=receiver_id)
	if request.user == user_visited:
		render(request, 'chat/alone.html')
	messages = Message.get_10_message(request.user, user_visited)
	context = {
		'messages': messages,
		'user_visited': user_visited
	}
	return render(request, 'chat/room.html', context)


def message_not_view(request, receiver_id):
	if request.is_ajax():
		user_visited = get_object_or_404(User, id=receiver_id)
		if request.user == user_visited:
			return render(request, 'chat/alone.html')
		messages = Message.get_messages_not_view(request.user, user_visited)
		return HttpResponse(json.dumps(messages), content_type="application/json")
	raise Http404


def read_message(request, receiver_id):
	if request.is_ajax():
		user_visited = get_object_or_404(User, id=receiver_id)
		if request.user == user_visited:
			return render(request, 'chat/alone.html')
		result = Message.set_read_message(request.user, user_visited)
		return HttpResponse(json.dumps(result), content_type="application/json")
	raise Http404


def send_message(request, receiver_id):
	if request.method == 'POST' and request.is_ajax():
		message = request.POST.get('content')
		instance_message = Message()
		user_visited = get_object_or_404(User, id=receiver_id)
		if request.user == user_visited:
			return render(request, 'chat/alone.html')
		result = Message.send_message(instance_message, request.user, user_visited, message)
		return HttpResponse(json.dumps(result), content_type="application/json")
	return HttpResponse(json.dumps(False), content_type="application/json")


def unread_message(request):
	if request.is_ajax():
		user_logged = request.user
		json_list = Message.get_unread_message(user_logged)
		if not bool(json_list):
			return HttpResponse(json.dumps(False), content_type="application/json")
		else:
			print(json_list)
			return HttpResponse(json.dumps(json_list), content_type="application/json")
	else:
		raise Http404






