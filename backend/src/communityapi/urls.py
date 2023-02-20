from django.urls import path
from .views import PostAPI

app_name = 'communityapi'  # pylint: disable=invalid-name

urlpatterns = [
    path('post/', PostAPI.as_view(), name='article'),
]
