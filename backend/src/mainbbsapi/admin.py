from django.contrib import admin
from .models import Reply, Article, CardNotice

# Register your models here.
admin.site.register(Reply)
admin.site.register(Article)
admin.site.register(CardNotice)
