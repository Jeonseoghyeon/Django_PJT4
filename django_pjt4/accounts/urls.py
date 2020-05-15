from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'accounts'

urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/follow', views.follow, name='follow'),
    path('<username>/profile_picture_update', views.profile_picture_update, name='profile_picture_update'),
    ]
