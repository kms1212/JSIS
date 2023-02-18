'''
Admin dashboard configuration for the authapi.

Registered models
-----------------
* UserAccount
'''

from django.contrib import admin
from .models import UserAccount

admin.site.register(UserAccount)
