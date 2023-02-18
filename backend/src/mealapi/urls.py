from django.urls import path
from .views import MealAPI

app_name = 'mealapi'  # pylint: disable=invalid-name

urlpatterns = [
    path('', MealAPI.as_view(), name='meal'),
]
