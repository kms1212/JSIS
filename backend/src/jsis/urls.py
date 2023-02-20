from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapi.urls')),
    path('notice/', include('noticeapi.urls')),
    path('bbsbase/', include('bbsbaseapi.urls')),
    path('file/', include('fileapi.urls')),
    path('class/', include('classapi.urls')),
    path('meal/', include('mealapi.urls')),
    path('community/', include('communityapi.urls')),
] + static('static/', document_root=settings.STATIC_ROOT)
