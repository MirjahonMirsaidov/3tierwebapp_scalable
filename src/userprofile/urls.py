from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from userprofile.views import MyTokenObtainPairView, ForgotPasswordView, ResetPasswordView, FileUploadGenericView, \
    FileListGenericView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('file-upload/', FileUploadGenericView.as_view(), name='file_upload'),
    path('file-list/', FileListGenericView.as_view(), name='file_list'),
]