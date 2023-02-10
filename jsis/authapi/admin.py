from django.contrib import admin
from .models import *

# Register your models here.
# add user model to admin console
admin.site.register(UserAccount)
admin.site.register(File)
