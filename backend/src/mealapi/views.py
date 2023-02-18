from rest_framework import generics, permissions
from rest_framework.response import Response
from django.utils import timezone
import requests
from utils.meal import request_meal
from .models import Meal, MealTime
from .serializers import MealSerializer

# Create your views here.
class MealAPI(generics.GenericAPIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request):
        serve_date = request.GET.get('mdate', timezone.now().strftime('%y%m%d'))
        meal_time = request.GET.get('mtime', None)

        if meal_time is None:
            current_hour = timezone.now().hour
            if current_hour < 10 or current_hour > 18:
                meal_time = MealTime.BREAKFAST
            elif current_hour < 14:
                meal_time = MealTime.LUNCH
            else:
                meal_time = MealTime.DINNER

        meal = Meal.objects.filter(serve_date=serve_date, meal_time=meal_time)

        if meal.exists():
            meal = meal.first()
            if meal.menus is None or meal.menus == {} or meal.menus == []:
                meal = None
        else:
            meal = request_meal(serve_date, meal_time)

        if meal is None:
            return Response(
                {
                    "message": "No meal found"
                },
                status=404
            )

        return Response(MealSerializer(meal).data, status=200)
