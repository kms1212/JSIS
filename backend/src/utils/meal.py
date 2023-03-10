"""
Utility functions for school meal database.

Functions
---------
:func:`filter_menuname`: Filter the menu name.
:func:`get_allergyinfo`: Get the allergy information.
:func:`get_meal`: Get the meal information.

Revision History
----------------
* 2023-02-18: Created by @kms1212.
"""

import re
import requests
from mealapi.models import Meal
from jsis.settings import NEIS_API_KEY, OE_CODE, SC_CODE

def filter_menuname(menuname):
    """
    Filter the menu name.

    Parameters / Return Values
    --------------------------
    :param menuname: Menu name. (ex. "맛살튀김&칠리소스(중앙)  (1.5.6.8.12.13.)")
    :returns: Filtered menu name. (ex. "맛살튀김&칠리소스(중앙)")
    """
    string = ''

    for idx, char in enumerate(menuname):
        if char.isdigit():
            if len(menuname) > idx + 2:
                if menuname[idx + 1] == '.' or menuname[idx + 2] == '.':
                    string = menuname[:idx]
                    break

    if string == '':
        string = menuname

    if string:
        if string[-1] == '(':
            string = string[:-1]

        if string[0] == '\t':
            string = string[1:]

        if string[-1] == '\n':
            string = string[:-1]

    while True:
        if string and string[-1] == ' ':
            string = string[:-1]
        else:
            break

    return string


def get_allergyinfo(menuname):
    """
    Get the allergy information.

    Parameters / Return Values
    --------------------------
    :param menuname: Menu name. (ex. "맛살튀김&칠리소스(중앙)  (1.5.6.8.12.13.)")
    :returns: Allergy information. (ex. [1, 5, 6, 8, 12, 13])
    """
    allergyinfo = re.findall(r'[0-9].{0,1}\.', menuname)

    return list(map(lambda str: int(str[:-1]), allergyinfo))


def request_meal(serve_date, meal_time):
    """
    Request meal data from the school meal database.

    Parameters / Return Values
    --------------------------

    :param serve_date: Serve date. (YYMMDD, %y%m%d)
    :param meal_time: Meal time. (1: Breakfast, 2: Lunch, 3: Dinner)
    :returns: Meal data.

    Description
    -----------

    This function requests meal data from the school meal database.
    It returns the meal data.

    Revision History
    ----------------
    * 2023-02-18: Created by @kms1212.
    """
    url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'

    params = {
        'KEY': NEIS_API_KEY,
        'Type': 'json',
        'ATPT_OFCDC_SC_CODE': OE_CODE,
        'SD_SCHUL_CODE': SC_CODE,
        'MLSV_YMD': serve_date,
        'MMEAL_SC_CODE': meal_time
    }

    response = requests.get(url, params=params, timeout=5)

    if response.status_code == 200:
        response = response.json()

        if response.get('mealServiceDietInfo') is None:
            # Meal data does not exist.
            meal = Meal.objects.create(
                serve_date=serve_date,
                meal_time=meal_time,
                menus=[],
            )

            return None

        resp_code = response['mealServiceDietInfo'][0]['head'][1]['RESULT']['CODE']
        if resp_code == 'INFO-000':
            # Meal data exists.
            menus_raw = response['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'].split('<br/>')
            menus = list(map(lambda menu: {
                'id': menu[0],
                'name': filter_menuname(menu[1]),
                'allergy': get_allergyinfo(menu[1])
                }, enumerate(menus_raw)))

            meal = Meal.objects.create(
                serve_date=serve_date,
                meal_time=meal_time,
                menus=menus,
            )

            return meal
        else:
            # Meal data does not exist.
            meal = Meal.objects.create(
                serve_date=serve_date,
                meal_time=meal_time,
                menus=[],
            )

    return None
