from django.contrib import admin
from django.urls import path, include
from knox.views import LogoutView as LogoutAPI
from .views import *

app_name = 'mainbbsapi'

urlpatterns = [
    path('article/', ArticleAPI.as_view(), name='article'),
    path('like/', ArticleLikeAPI.as_view(), name='like'),
]