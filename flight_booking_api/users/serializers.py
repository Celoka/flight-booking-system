from rest_framework import serializers
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
        fields = ("first_name", "last_name", "email","password",)

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password')
