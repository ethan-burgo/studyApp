from django import forms
from . models import User, Goals, Schedule, Schedule_Items
from django.contrib.auth.models import User
from django.conf import settings


class usersName(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]

class goals(forms.ModelForm):
    class Meta:
        model = Goals
        fields = [
            'title',
            'short_term',
            'mid_term',
            'long_term',
            'favorite'
        ]

class carry_goals(forms.ModelForm):
    class Meta:
        model = Goals
        fields = [
            'short_time',
            'mid_time',
            'long_time'
        ]

class get_goals(forms.Form):
    data_title = forms.CharField(max_length=30)

class edit_goals(forms.ModelForm):
    class Meta:
        model = Goals
        fields = [
            'title',
            'short_term',
            'short_time',
            'mid_term',
            'mid_time',
            'long_term',
            'long_time',
            'favorite'
        ]

class create_schedule(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = [
            'title',
            'favorite'
        ]

class TimeInput(forms.TimeInput):
    input_type = 'time'

class schedule_details(forms.ModelForm):
    class Meta:
        model = Schedule_Items
        widgets = {
            'start_time': TimeInput(),
            'end_time': TimeInput()
        }
        fields = [
            'day_name',
            'start_time',
            'end_time',
            'activity',
            'description',
        ]

class get_schedule(forms.Form):
    data_title = forms.CharField(max_length=30)
