from __future__ import unicode_literals

from django.db import models
from accounts.models import UserProfile


# We assume that all the states and cities can be stored in the database in a same table.
class State(models.Model):
	name = models.CharField(max_length = 50)
	abbreviation = models.CharField(max_length = 2)

	def __str__(self):
		return self.name


class City(models.Model):
	name = models.CharField(max_length = 50)
	state = models.CharField(max_length = 2)
	longitude = models.CharField(max_length = 20)
	latitude = models.CharField(max_length = 20)
	zipcode = models.CharField(max_length = 5)
	county = models.CharField(max_length = 50)

	def __str__(self):
		return self.name


class UserAddress(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	user_state = models.ForeignKey(State, related_name='user_state')
	user_city = models.ForeignKey(City, related_name='user_city')
	zipcode = models.PositiveIntegerField(blank = False)

