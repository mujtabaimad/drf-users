

from django.urls import path
from authentication.views import RegisterView, VerifyEmailView


urlpatterns = [
    path(r'registar/', RegisterView.as_view(), name="register"),
    path(r'verify-email/', VerifyEmailView.as_view(), name="verify-email"),
]
