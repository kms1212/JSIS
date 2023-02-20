from django.urls import path
from .views import NoticeAPI

app_name = 'noticeapi'  # pylint: disable=invalid-name

urlpatterns = [
    path('', NoticeAPI.as_view(), name='notice'),
]
