from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields=['first_name', 'last_name', 'email', 'password']
    
    def validate(self, attrs):
        emailInput=attrs.get('email', '')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class VerifyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, write_only= True)
    password = serializers.CharField(min_length=8, write_only= True)
    token = serializers.EmailField(read_only=True)


    class Meta:
        model = User
        fields = ['email', 'password', 'token']
    
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email = email, password= password)
        if(not user):
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'token': user.access_token()
        }



class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class AuthenticatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name', 'email', 'is_verified']


class UnAuthenticatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'is_verified']

