from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
	sender = models.ForeignKey(User, related_name='sender_message')
	receiver = models.ForeignKey(User, related_name='receiver_message')
	content = models.TextField(verbose_name='Message')
	time = models.DateTimeField(default=timezone.now)
	visualized = models.BooleanField(default=False)

	def __str__(self):
		return 'Message from ' + self.sender.username + ' to ' + self.receiver.username

	def format_date_chat(self, data):
		return self.less_than_10(data.day) + "/" + self.less_than_10(data.month) + "/" + str(
			data.year) + " at " + self.less_than_10(data.hour) + ":" + self.less_than_10(
			data.minute) + ":" + self.less_than_10(data.second)

	@staticmethod
	def less_than_10(n):
		if n < 10:
			return "0" + str(n)
		return str(n)

	def send_message(self, user_logged, user_visited, content):
		new_message = Message()
		new_message.sender = user_logged
		new_message.receiver = user_visited
		new_message.content = content
		new_message.save()
		return [new_message.content, self.format_date_chat(self.time), str(user_logged.user_profile.get_mugshot_url())]

	@staticmethod
	def get_10_message(user_logged, user_visited):
		message_list = list()

		message_logged = Message.objects.filter(sender=user_logged, receiver=user_visited, visualized=True)
		message_visited = Message.objects.filter(sender=user_visited, receiver=user_logged, visualized=True)

		for message in message_logged:
			message_list.append(message)

		for message in message_visited:
			message_list.append(message)

		message_list.sort(key=lambda x: x.time)

		return message_list[::-1][0:10][::-1]

	@staticmethod
	def get_messages_not_view(user_logged, user_visited):
		message_list = list()
		message_visited = Message.objects.filter(sender=user_visited, receiver=user_logged)

		for message in message_visited:
			if not message.visualized:
				print(message.visualized)
				message_list.append(([message.content], ["{}/{} - {}:{}:{}".format(
					message.time.month, message.time.day, message.time.hour, message.time.minute, message.time.second
				)], [str(user_visited.user_profile.get_mugshot_url())]))

		return message_list

	@staticmethod
	def set_read_message(user_logged, user_visited):
		message_visited = Message.objects.filter(sender=user_visited, receiver=user_logged)

		for message in message_visited:
			if not message.visualized:
				message.visualized = True
				message.save()

		return True

	@staticmethod
	def get_unread_message(user_logged):
		unread_message_list = []
		unread_message = Message.objects.filter(receiver=user_logged, visualized=False)

		for message in unread_message:
			unread_message_list.append(message)
		unread_message_list.sort(key=lambda x: x.sender.username)

		msg_dic = {}
		json_list = list()

		for message in unread_message:
			sender = message.sender
			name = msg_dic.get(sender)
			if name is None:
				msg_dic[sender] = [message]
			else:
				msg_dic[sender].append(message)

		for sender, msg_list in msg_dic.items():
			json_list.append(([sender.username], [sender.id], [len(msg_list)]))

		return json_list










