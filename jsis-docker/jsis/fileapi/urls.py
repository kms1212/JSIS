from django.contrib import admin
from django.urls import path, include
from knox.views import LogoutView as LogoutAPI
from .views import *

app_name = 'fileapi'

urlpatterns = [
    path('', FileAPI.as_view(), name='file'),
    path('info/', FileInfoAPI.as_view(), name='file_info'),
]
