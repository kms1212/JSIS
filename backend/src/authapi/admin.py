from django.contrib import admin
from .models import UserAccount

# Register your models here.
# add user model to admin console
admin.site.register(UserAccount)
