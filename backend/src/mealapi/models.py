from django.db import models


class MealTime(models.IntegerChoices):
    """
    Meal time

    Choices
    -------
    :BREAKFAST: Breakfast
    :LUNCH:     Lunch
    :DINNER:    Dinner

    Revision History
    ----------------
    * 2020-02-18: Created by @kms1212.
    """
    BREAKFAST = 1, '조식'
    LUNCH = 2, '중식'
    DINNER = 3, '석식'


class Meal(models.Model):
    """
    Meal

    Fields
    ------
    :mealid:        Meal ID
    :serve_date:    Serve date
    :meal_time:     Meal time

    Revision History
    ----------------
    * 2020-02-18: Created by @kms1212.
    """
    mealid = models.AutoField(primary_key=True)
    serve_date = models.CharField(max_length=10)
    meal_time = models.IntegerField(choices=MealTime.choices)
    menus = models.JSONField(default=dict)

    def __str__(self):
        return str(self.serve_date) + ' ' + str(self.meal_time)
