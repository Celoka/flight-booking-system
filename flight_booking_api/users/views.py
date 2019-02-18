from django.shortcuts import render
from django.contrib.auth import authenticate, login

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status,APIView
from rest_framework_jwt.settings import api_settings

from .models import User
from .serializers import UserSerializer,TokenSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegisterUserView(generics.CreateAPIView):
    """
    POST auth/register
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        first_name = request.data.get("first_name", "")
        last_name  = request.data.get("last_name", "")
        email      = request.data.get("email", "")
        password   = request.data.get("password", "")
        if not first_name and not last_name and not email and not password:
            return Response(
                data={
                    "message": "All user field credentials are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )
