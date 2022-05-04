from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):

    def create_user(self, email, password,first_name=None, last_name=None):
        if(email is None):
            raise TypeError('email should not be None')
        if(password is None):
            raise TypeError('password should not be None')
        user = self.model( email= self.normalize_email(email),first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self,  email, password, first_name = None, last_name = None):
        if(email is None):
            raise TypeError('email should not be None')
        if(password is None):
            raise TypeError('password should not be None')
            
        user = self.create_user(email, password, first_name, last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, )
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def access_token(self):
        refresh_token = RefreshToken.for_user(self)
        return  str(refresh_token.access_token)