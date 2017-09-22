# -*- coding: utf-8 -*-

from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.conf import settings
from django.template.defaultfilters import date as dj_date
from django.utils.translation import ugettext as _
from django.db.models import Q


class Dialog(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"), related_name="selfDialogs")
    opponent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog opponent"))

    def __str__(self):
        return _("Chat with ") + self.opponent.username


class Message(TimeStampedModel, SoftDeletableModel):
    dialog = models.ForeignKey(Dialog, verbose_name=_("Dialog"), related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="messages")
    text = models.TextField(verbose_name=_("Message text"))
    visualized = models.BooleanField(default=False, null=False)
    all_objects = models.Manager()

    def get_formatted_create_datetime(self):
        return dj_date(self.created, settings.DATETIME_FORMAT)

    def __str__(self):
        return self.sender.username + "(" + self.get_formatted_create_datetime() + ") - '" + self.text + "'"

    @staticmethod
    def get_unread_message(user_logged):
        unread_message_list = []
        dialogs = Dialog.objects.filter(Q(owner=user_logged) | Q(opponent=user_logged))
        # print(dialogs)
        for dialog in dialogs:
            unread_message = Message.objects.filter(dialog=dialog, visualized=False).exclude(sender=user_logged)

            for message in unread_message:
                unread_message_list.append(message)

        unread_message_list.sort(key=lambda x: x.sender.username)

        msg_dic = {}
        json_list = list()

        for message in unread_message_list:
            sender = message.sender
            name = msg_dic.get(sender)
            if name is None:
                msg_dic[sender] = [message]
            else:
                msg_dic[sender].append(message)

        for sender, msg_list in msg_dic.items():
            json_list.append(([sender.username], [sender.id], [len(msg_list)]))

        return json_list
