from django.urls import path
from authentication.views import ChangePasswordView, LoginView, RegisterView, UserViewSet, VerifyEmailView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls
urlpatterns.extend([
    path(r'registar/', RegisterView.as_view(), name="register"),
    path(r'verify-email/', VerifyEmailView.as_view(), name="verify-email"),
    path(r'login/', LoginView.as_view(), name="login"),
    path(r'change-password/', ChangePasswordView.as_view(), name="change-password"),
])
