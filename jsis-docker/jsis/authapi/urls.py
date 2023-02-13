from django.contrib import admin
from django.urls import path, include
from knox.views import LogoutView as LogoutAPI
from .views import *

app_name = 'authapi'

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('user/', UserAPI.as_view(), name='user'),
    path('validate_email/<str:uid>/<str:token>/', EmailValidationAPI.as_view(), name='validate_email'),
]
