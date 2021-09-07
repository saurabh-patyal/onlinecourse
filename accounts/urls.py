from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
     path('login', views.login , name='login'),
     path('signup', views.signup , name='signup'),
     path('logout', views.user_logout , name='user_logout'),
     path('changeuserpassword', views.changeuserpassword , name='changeuserpassword'),
     path('UpdateProfile', views.UpdateProfile , name='UpdateProfile'),
]
