from rest_framework import serializers
import utils.file as fileutils
from .models import Meal


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('serve_date', 'meal_time', 'menus')
