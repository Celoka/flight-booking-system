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
    def _create_user(self,email,password=None,is_admin=False,is_staff=False,is_active=True):
        if not email:
            raise ValueError('Users must have a valid email')
        if not password:
            raise ValueError('Users must have a password')

        user_obj = self.model(
           email=self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.save(using=self._db)
        return user_obj
    
    def create_user(self,first_name,last_name,email,password):
        user = self._create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_staff=False
        user.is_superuser=False
        user.is_admin=False
        user.is_active=True
        user.save(using=self._db)
        return user

    # create super admin user
    def create_superuser(self,email,password,first_name=None,last_name=None):
        user = self._create_user(
            email,
            password=password,
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
    first_name   = models.CharField(max_length=20, blank=True, null=True)
    last_name    = models.CharField(max_length=20,blank=True, null=True)
    email        = models.EmailField(_('email address'), unique=True)
    photo        = models.ImageField(upload_to='uploads', blank=True)
    is_staff     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = UserManager()

    def __unicode__(self):
        return self.email



# This gets the user id from the User object
def get_user(user_id):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None
