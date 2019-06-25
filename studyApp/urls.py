from django.contrib import admin
from django.urls import path, re_path, include

from study import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('account/', include('django.contrib.auth.urls')),
    re_path(r'^$', views.home, name='home'),
    re_path(r'schedules', views.schedulePage, name='schedules'),
    re_path(r'sign in', views.signInPage, name='sign in'),
    re_path(r'login', views.login_view, name='login'),
    re_path(r'logout', views.logout_view, name='logout'),
    re_path(r'user details', views.userDetails_view, name='user details'),
    re_path(r'set goals', views.setGoals_view, name='set goals'),
    re_path(r'your goals', views.configGoals_view, name='your goals'),
    re_path(r'schedule_adding', views.schedule_adding, name='schedule_adding'),
    re_path(r'cool', views.configSchedules_view, name='cool'),
    re_path(r'Edit_Schedules', views.EditSchedules_view, name='Edit_Schedules'),
    re_path(r'carry_goals', views.carryGoals_view, name='carry_goals'),


]
