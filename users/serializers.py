from rest_framework import serializers, validators
from .models import User


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    """
    This serializes the user object
    """
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id','username','first_name', 'last_name', 'email','password')


class UserLoginSerializer(serializers.ModelSerializer):
    """
    This serializes the user login object
    """
    class Meta:
        model = User
        fields = ('id','username','password')

class ImageUploadSerializer(serializers.ModelSerializer):
    """
    Handles file/image upload by a user
    """
    class Meta:
        model = User
        fields = ('id','photo','updated_at')
