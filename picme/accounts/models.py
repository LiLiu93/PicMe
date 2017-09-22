from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
	gender_choices = (
		('M', 'Male'),
		('F', 'Female'),
		('U', 'Unknown')
	)

	user = models.OneToOneField(User, 
		on_delete=models.CASCADE,
		unique=True,
		verbose_name=_('user'),
		related_name='user_profile')

	nick_name = models.CharField(max_length=30)

	# User Description
	description = models.CharField(max_length=100,blank=True,null=True)
	
	gender = models.CharField(max_length=1, choices=gender_choices, default='U') 

	# Follow others
	follows = models.ManyToManyField(User, blank=True)

	def __str__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		if not self.nick_name:
			self.nick_name = self.user.username
		super(UserProfile, self).save(*args, **kwargs)