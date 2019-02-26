from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save

import os

# Create your models here.

class UserManager(BaseUserManager):
    """
    Manages and creates different type of users
    """
    use_in_migrations = True
    
    # create a user
    def _create_user(self,email,
                    password=None,is_admin=False,
                    is_staff=False,is_active=True,**extra_fields):
        if not email:
            raise ValueError('Users must have a valid email')
        if not password:
            raise ValueError('Users must have a password')

        user_obj = self.model(
           email=self.normalize_email(email),
           **extra_fields
        )
        user_obj.set_password(password)
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.is_active=is_active
        user_obj.save(using=self._db)
        return user_obj
    
    def create_user(self,email,password,**extra_fields):
        user = self._create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_superuser=False
        user.save(using=self._db)
        return user

    # create super admin user
    def create_superuser(self,email,password,
                        first_name=None,last_name=None,
                        **extra_fields):
        user = self._create_user(
            email,
            password=password,
            **extra_fields
            )
        user.is_superuser=True
        user.is_admin=True
        user.is_staff=True
        user.is_active=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin): 
    """
    User model
    """
    username = models.CharField(max_length=20, blank=True,unique=True,null=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20,blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    photo = models.ImageField(upload_to='uploads', blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name','email', 'password']

    objects = UserManager()

    def __str__(self):
        return self.username
