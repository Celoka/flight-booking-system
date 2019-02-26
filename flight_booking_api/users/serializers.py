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
    def validate_username(self, value):
        ModelClass = self.Meta.model
        if ModelClass.objects.filter(username=value).exists():
            raise serializers.ValidationError('This user is registered')
        return value

    def validate_email(self, value):
        ModelClass = self.Meta.model
        if ModelClass.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
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
