from django.urls import path
from authentication.views import ChangePasswordView, LoginView, RegisterView, VerifyEmailView


urlpatterns = [
    path(r'registar/', RegisterView.as_view(), name="register"),
    path(r'verify-email/', VerifyEmailView.as_view(), name="verify-email"),
    path(r'login/', LoginView.as_view(), name="login"),
    path(r'change-password/', ChangePasswordView.as_view(), name="change-password"),
]
