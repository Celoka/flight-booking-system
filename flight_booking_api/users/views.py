from django.shortcuts import render
from django.contrib.auth import login

from rest_framework import generics,permissions,exceptions
from rest_framework.response import Response
from rest_framework.views import status,APIView
from rest_framework.exceptions import ParseError
from rest_framework_jwt.settings import api_settings
from rest_framework.parsers import MultiPartParser,FormParser

from .models import User
from .helper import (check_if_exist,
                    validate_username,
                    validate_password,
                    validate_non_empty_input,
                    validate_login_input)

from .serializers import (UserSerializer,
                        TokenSerializer,
                        UserLoginSerializer,
                        ImageUploadSerializer)


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegisterUserView(generics.CreateAPIView):
    """
    POST auth/register
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username   = request.data.get("username", "default")
        first_name = request.data.get("first_name", "")
        last_name  = request.data.get("last_name", "")
        email      = request.data.get("email", "default")
        password   = request.data.get("password", "")

        validate_username(username)
        validate_password(password)
        check_if_exist(email, username)

        new_user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )


class LoginView(generics.CreateAPIView):
    """
    Post auth/login
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class   = UserLoginSerializer

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        user = validate_login_input(request, request.data)
        if user is not None:
            login(request, user)
            token_serializer = TokenSerializer(
                data={
                    "token": jwt_encode_handler(
                        jwt_payload_handler(user)
                    )
                }
            )
            if token_serializer.is_valid():
                serializer = UserLoginSerializer(user)
                return Response(
                    data={
                        "id": serializer.data.get('id'),
                        "username": serializer.data.get('username'),
                        "token":token_serializer.data
                    },
                    status=status.HTTP_200_OK)
        return Response(data={
            "error":"Unauthorized operation"
        },
        status=status.HTTP_401_UNAUTHORIZED)

class ImageUploadViewSet(APIView):
    """
    User image upload
    """
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ImageUploadSerializer

    def post(self, request, *args, **kwargs):
        try:
            photo = request.data.get('photo')
        except KeyError:
            return ParseError('Photo field cannot be empty')
        user = request.user
        user.photo = photo
        user.save()
        serializer = ImageUploadSerializer(user)
        return Response(data={
                "message": "Successful Upload",
                "data":serializer.data
            },
            status=status.HTTP_201_CREATED)

    def delete(self,request, *args, **kwargs):
        user = request.user
        user.photo.delete(save=True)
        return Response(data={
                "message": "Delete successful"
            },
            status=status.HTTP_204_NO_CONTENT)
