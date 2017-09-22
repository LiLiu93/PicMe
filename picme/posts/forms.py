from django import forms
from django.shortcuts import get_object_or_404
from .models import Post
from address.models import City
from django.utils.translation import ugettext as _

import logging

logger = logging.getLogger(__name__)


MAX_UPLOAD_SIZE = 20971520


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = (
			'post_title',
			'post_description',
			'post_picture',
			'post_state',
			'post_city'
		)

		labels = {
			"post_title": _("Title"),
			"post_description": _("Description"),
			"post_picture": _("Upload")
		}

	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)

		self.initial['post_state'] = 10101010101
		self.fields['post_state'].empty_label = "Please Choose"

		self.fields['post_city'].choices = []

	def clean_post_picture(self):
		file = self.cleaned_data['post_picture']

		supported_image_type = ['image/jpeg', 'image/pjpeg', 'image/png', 'image/gif']

		supported_video_type = ['video/mp4', 'video/webm', 'video/ogg']

		if not file.content_type or not (file.content_type in supported_video_type or file.content_type in supported_image_type):
			raise forms.ValidationError(_('File type is not supported'))

		if file.size > MAX_UPLOAD_SIZE:
			raise forms.ValidationError(_('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE)))
		return file

class EditPostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['post_title','post_description','post_state','post_city']

	def __init__(self , *args, **kwargs):
		city = kwargs.pop('city', None)
		super(EditPostForm, self).__init__(*args, **kwargs)
		if city :
			logger.debug("[city_id] = " + str(city))
			self.fields['post_city'].choices = [(city.id, city.name)]
