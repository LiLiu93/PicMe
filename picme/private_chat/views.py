from django.views import generic
from django.shortcuts import HttpResponse

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from . import models
from . import utils
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User

import json


class DialogListView(generic.ListView):
    template_name = 'dialogs.html'
    model = models.Dialog
    ordering = 'modified'

    def get_queryset(self):
        dialogs = models.Dialog.objects.filter(Q(owner=self.request.user) | Q(opponent=self.request.user))
        return dialogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.kwargs.get('username'):
            # TODO: show alert that user is not found instead of 404
            user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
            dialog = utils.get_dialogs_with_user(self.request.user, user)
            if len(dialog) == 0:
                dialog = models.Dialog.objects.create(owner=self.request.user, opponent=user)
            else:
                dialog = dialog[0]
            context['active_dialog'] = dialog
        else:
            context['active_dialog'] = self.object_list[0]
        if self.request.user == context['active_dialog'].owner:
            context['opponent_username'] = context['active_dialog'].opponent.username
        else:
            context['opponent_username'] = context['active_dialog'].owner.username
        context['ws_server_path'] = 'ws://{}:{}/'.format(
            settings.CHAT_WS_SERVER_HOST,
            settings.CHAT_WS_SERVER_PORT,
        )
        return context


def set_read_message(request, username):
    other = User.objects.get (username=username)
    dialog = models.Dialog.objects.filter (
        Q (owner=request.user, opponent=other) | Q (owner=other, opponent=request.user)
    )
    messages = models.Message.objects.filter (dialog=dialog[0], sender=other, visualized=False)
    for message in messages:
        message.visualized = True
        message.save()

    return HttpResponse("success")


def unread_message(request):
    if request.is_ajax():
        user_logged = request.user
        json_list = models.Message.get_unread_message(user_logged)
        if not bool(json_list):
            return HttpResponse(json.dumps(False), content_type="application/json")
        else:
            print(json_list)
            return HttpResponse(json.dumps(json_list), content_type="application/json")
    else:
        pass

