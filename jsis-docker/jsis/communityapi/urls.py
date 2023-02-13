from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'communityapi'

urlpatterns = [
    path('article/', ArticleAPI.as_view(), name='article'),
    path('like/', ArticleLikeAPI.as_view(), name='like'),
]