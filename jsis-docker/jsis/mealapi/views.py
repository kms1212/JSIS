from rest_framework import generics, status, permissions
from rest_framework.response import Response

from django.http.response import HttpResponse

from jsis.settings import NEIS_API_KEY
import utils.file as fileutils

# Create your views here.
class MealView(generics.GenericAPIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request):
        oe_code = 'C10'
        sc_code = '7150107'
