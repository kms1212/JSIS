from django.urls import path
from .views import FileAPI, FileInfoAPI

app_name = 'fileapi'  # pylint: disable=invalid-name

urlpatterns = [
    path('', FileAPI.as_view(), name='file'),
    path('info/', FileInfoAPI.as_view(), name='file_info'),
]
