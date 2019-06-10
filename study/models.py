from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

class User(models.Model):
    userName = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class Schedule(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True)
    favorite = models.BooleanField(default=False)

    def get_queryset(self):
        return Post.objects.all()

    def __str__(self):
        return self.title

class WeekDay(models.Model):
    day_name = models.CharField(max_length=50)
    day_order = models.IntegerField()

    def get_queryset(self):
        return Post.objects.all()

    def __str__(self):
        return self.day_name

class Schedule_Items(models.Model):
    title = models.ForeignKey(
        Schedule, on_delete=models.CASCADE)
    day_name = models.ForeignKey(
        WeekDay, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity = models.CharField(max_length=30)
    description = models.CharField(max_length=70)

    def get_queryset(self):
        return Post.objects.all()

    def __str__(self):
        return self.title.title


class Goals(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True)
    short_term = models.CharField(max_length=50)
    mid_term = models.CharField(max_length=50)
    long_term = models.CharField(max_length=50)
    reflection = models.CharField(max_length=100, null = True)
    favorite = models.BooleanField(default=False)
    time = models.CharField(max_length=30, null = True)


    def get_queryset(self):
        return Post.objects.all()

    def __str__(self):
        return self.title
