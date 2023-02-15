from django.urls import path
from .views import ArticleAPI, ArticleLikeAPI

app_name = 'mainbbsapi'  # pylint: disable=invalid-name

urlpatterns = [
    path('article/', ArticleAPI.as_view(), name='article'),
    path('like/', ArticleLikeAPI.as_view(), name='like'),
]
