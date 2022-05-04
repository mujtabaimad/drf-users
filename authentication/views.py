from rest_framework import generics, status
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from django.contrib.sites.shortcuts import get_current_site

from authentication.serializers import AuthenticatedUserSerializer, ChangePasswordSerializer, LoginSerializer, UnAuthenticatedUserSerializer, UserSerializer, VerifyEmailSerializer
from .models import User
from authentication.utils import sendRegistrationEmail


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        userData = serializer.data
        user = User.objects.get(email = userData['email'])
        try:
            jwtAccessToken = str(RefreshToken.for_user(user).access_token)
            confirmationLink = 'http://'+ get_current_site(request).domain +reverse('verify-email')+"?token="+ jwtAccessToken
            first_name = user.first_name
            sendRegistrationEmail(userData['email'],first_name,  confirmationLink)
            return Response(userData, status=status.HTTP_201_CREATED)
        except Exception as e:
            user.delete()
            return Response({'error': 'general_error', 'error_message':str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            serializer = self.serializer_class(instance = user)
            userData = serializer.data
            return Response(userData, status=status.HTTP_201_CREATED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response({'error': 'link_expired','error_message': 'Activation link expired', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'invalid_link', 'error_message':'Invalid link', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'general_error', 'error_message':str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({'success': True}, status=status.HTTP_200_OK)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated:
            return AuthenticatedUserSerializer
        else:
            return UnAuthenticatedUserSerializer