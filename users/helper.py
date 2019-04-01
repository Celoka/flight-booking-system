import re
from users.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.views import status


def validate_username(username):
    """
    Validate username 
    """
    if re.search(r'([^a-zA-Z/._\d+])', username) is None:
        return username
    raise serializers.ValidationError(
        'Username can only contain alphanumeric characters and . or _.'
    )

def validate_password(password):
    """
    Validate password
    """
    if re.search(r'(^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$_!%*?&]{8,}$)', password) is not None:
        return password
    raise serializers.ValidationError(
        'Password contain a lowercase, an uppercase, a number & a special character and should be atleast 8 characters long'
    )

def check_if_exist(email,username):
    """
    Validate email and username
    """
    if User.objects.filter(email=email).exists()\
        or User.objects.filter(username=username).exists():
        raise serializers.ValidationError('Username or Email already exist')

def validate_login_input(request, validated_data):
    """
    Validate login input fields
    """
    username    = validated_data.get("username")
    password = validated_data.get("password")
    if username and password:
        return authenticate(request, username=username, password=password)
    message = "Enter a valid login credential"
    raise serializers.ValidationError(message)
