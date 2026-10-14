from django.contrib import admin
from .models import Booking, Route, Schedule
admin.site.register([Route, Schedule, Booking])

