from django.contrib import admin

from .models import Goals, Schedule_Items, Schedule, WeekDay
admin.site.register(Goals)
admin.site.register(Schedule)
admin.site.register(Schedule_Items)
admin.site.register(WeekDay)
