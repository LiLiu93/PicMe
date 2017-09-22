from django.shortcuts import render
from django.http import HttpResponse

from .models import State, City

import json

import logging
logger = logging.getLogger(__name__)

# Create your views here.

def getCityList(request):
	code = request.GET.get('code', None)
	state = State.objects.get(pk=code)
	cities = City.objects.filter(state=state.abbreviation)
	logging.debug("[cities] = " + str(cities))

	list = []
	for city in cities:
		c = {}
		c['name'] = city.name
		c['code'] = city.pk
		list.append(c)

	return HttpResponse(json.dumps(list),content_type = "application/json;charset=utf-8")
