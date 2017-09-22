from django.contrib import admin

# Register your models here.
from .models import State, City, UserAddress

admin.site.register(State)
admin.site.register(City)
admin.site.register(UserAddress)