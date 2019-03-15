from django.shortcuts import render
from django.contrib.auth import login

from rest_framework import generics,permissions,exceptions
from rest_framework.decorators import api_view,permission_classes
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


@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def index(request,*args,**kwargs):
    return Response(data={
               'message': 'Welcome to flight booking system'
            },
            status=status.HTTP_200_OK)


class RegisterUserView(generics.CreateAPIView):
    """
    POST auth/register
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
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
    authentication_classes = ()
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
            "message":"User does not exist"
        },
        status=status.HTTP_401_UNAUTHORIZED)

class ImageUploadViewSet(APIView):
    """
    User image upload
    """
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ImageUploadSerializer
    queryset = User.objects.all()
    serializer_class = ImageUploadSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.get('photo')
        if data is None or data == "":
            raise exceptions.ValidationError("Field must not be empty")
        else:
            user = request.user
            user.photo = data
            user.save()
            serializer = ImageUploadSerializer(user)
            return Response(data={
                "message": "Successful Upload",
                "data":serializer.data
            },
            status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        pk=kwargs["pk"]
        try:
            user = self.queryset.get(pk=pk)
            serializer = ImageUploadSerializer(user)
            return Response(data={
                "message": "Success",
                "data":serializer.data
            },
            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                data={"message":"User object not found"},
                status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        data = request.data.get("photo")
        if data is None or data == "":
            raise exceptions.ValidationError("Field must not be empty")
        try:
            user = self.queryset.get(pk=pk)
            serializer = ImageUploadSerializer()
            updated_photo = serializer.update(user, data)
            return Response(data={
                "message": "Update was successful",
                "data": ImageUploadSerializer(updated_photo).data
            },
            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                data={"message":"User object not found"},
                status=status.HTTP_404_NOT_FOUND)

    def delete(self,request, *args, **kwargs):
        pk=kwargs["pk"]
        try:
            user = self.queryset.get(pk=pk)
            user.photo.delete(save=True)
            return Response(data={
                "message": "Delete successful"
            },
            status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                data={"message":"User object not found"},
                status=status.HTTP_404_NOT_FOUND)
