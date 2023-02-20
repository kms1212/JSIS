from django.urls import path
from .views import LikeAPI, ReplyAPI

app_name = 'bbsbaseapi'  # pylint: disable=invalid-name

urlpatterns = [
    path('like/', LikeAPI.as_view(), name='like'),
    path('reply/', ReplyAPI.as_view(), name='reply'),
]
