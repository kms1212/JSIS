from rest_framework import generics, permissions

# Create your views here.
class MealView(generics.GenericAPIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, _request):
        _oe_code = 'C10'
        _sc_code = '7150107'
