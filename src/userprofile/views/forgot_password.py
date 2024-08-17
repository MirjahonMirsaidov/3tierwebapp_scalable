from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from userprofile.serializers.forgot_password import ForgotPasswordSerializer, ResetPasswordSerializer


class ForgotPasswordView(CreateAPIView):
    """
    Forgot password view
    """
    serializer_class = ForgotPasswordSerializer


class ResetPasswordView(CreateAPIView):
    """
    Reset password view
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = IsAuthenticated,



