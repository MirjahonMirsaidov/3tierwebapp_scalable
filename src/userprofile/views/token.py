from rest_framework_simplejwt.views import TokenObtainPairView

from userprofile.serializers.token import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
