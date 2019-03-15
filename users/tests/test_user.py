
import json
import os
import tempfile

from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.test import TestCase

from PIL import Image

# Create your tests here.
from rest_framework.test import APIClient,APITestCase, APIRequestFactory
from rest_framework.views import status

from users.models import User

client = APIClient()

def upload_a_file(photo=""):
        url = reverse(
            "file-upload",
            kwargs={
                "version": "v1"
            }
        )
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)

        return client.post(
            url,
            {"photo":tmp_file},
            format="multipart"       
     )


class BaseViewTest(APITestCase):
    pass


class TestHomeRoute(APITestCase):

    def test_home_route(self):
        url = reverse("home-route", kwargs={"version": "v1"})
        response = client.get(url,content_type='application/json')
        self.assertEqual(response.data["message"], 'Welcome to flight booking system')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserModelTest(APITestCase):

    def setUp(self):
        self.a_user = User.objects.create_user(
            username="Luska",
            first_name="Eloka",
            last_name="Chima",
            email="eloka.chima@email.com",
            password="EUROCKF$1"
        )
  
    def test_user_is_created(self):
        self.assertEqual(self.a_user.username, "Luska")
        self.assertEqual(self.a_user.first_name, "Eloka")
        self.assertEqual(self.a_user.last_name, "Chima")
        self.assertEqual(self.a_user.email, "eloka.chima@email.com")


class RegisterUserTest(TestCase):

    def setUp(self):
        self.valid_credentials = {
            "username": "West",
            "first_name": "West",
            "last_name": "John",
            "email": "west.john@email.com",
            "password": "Wetdgfj$1"
        }
        self.bad_format_details = {
            "username": "West",
            "first_name": "John",
            "password": "2"
        }

    def test_register_a_user(self):
        url = reverse("auth-register", kwargs={"version": "v1"})
        response = client.post(url, data=json.dumps(self.valid_credentials), 
                                content_type='application/json')
        self.assertEqual(response.data["username"],"West")
        self.assertEqual(response.data["first_name"],"West")
        self.assertEqual(response.data["last_name"],"John")
        self.assertEqual(response.data["email"],"west.john@email.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_user_password(self):
        url = reverse("auth-register",kwargs={"version": "v1"})
        response = client.post(url, data=json.dumps(self.bad_format_details),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Password contain a lowercase, an uppercase, a number & a special character and should be atleast 8 characters long')

    def test_valid_user_name(self):
        url = reverse("auth-register",kwargs={"version": "v1"})
        invalid_credentials = {
            "username": "99#=",
            "first_name": "West",
            "last_name": "John",
            "email": "west.john@email.com",
            "password": "Wetdgfj$1"
        }
        response = client.post(url, data=json.dumps(invalid_credentials),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Username can only contain alphanumeric characters and . or _.')


class LoginUSerTest(BaseViewTest):

    def setUp(self):
        self.valid_credentials = dict(
            username='West',
            first_name='West',
            last_name='John',
            email='west.john@email.com',
            password='Wetdgfj$1'
        )
        self.user_details = {
            "username":"West",
            "password":"Wetdgfj$1"
        }
        url = reverse("auth-register", kwargs={"version": "v1"})
        client.post(url, data=json.dumps(self.valid_credentials), 
                                content_type='application/json')

    def test_login_user_with_valid_credentials(self):
        url = reverse("auth-login",kwargs={"version": "v1"})
        response = client.post(
            url,
            data=json.dumps(self.user_details),
            content_type="application/json"
        )
        self.assertIn("token", response.data["token"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_with_invalid_credentials(self):
        invalid_credentials = dict(
            username='',
            password='Wetdgfj$1'
        )
        url = reverse("auth-login",kwargs={"version": "v1"})
        response = client.post(
            url,
            data=json.dumps(invalid_credentials),
            content_type="application/json"
        )
        self.assertEqual(response.data[0], "Enter a valid login credential")

    def test_user_login_with_wrong_credential(self):
        wrong_credentials = dict(
            username='tes',
            password='Wetdgfj$1'
        )
        url = reverse("auth-login",kwargs={"version": "v1"})
        response = client.post(
            url,
            data=json.dumps(wrong_credentials),
            content_type="application/json"
        )
        self.assertEqual(response.data['message'], "User does not exist")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FileUpload(BaseViewTest):
    """
    Tests for user file upload
    """
    def setUp(self):
        self.valid_credentials = dict(
            username='West',
            first_name='West',
            last_name='John',
            email='west.john@email.com',
            password='Wetdgfj$1'
        )
        self.user_details = {
            "username":"West",
            "password":"Wetdgfj$1"
        }
        client.post(
            reverse("auth-register", kwargs={"version": "v1"}),
            data=json.dumps(self.valid_credentials), 
                            content_type='application/json')
        self.user = client.post(
            reverse("auth-login",kwargs={"version": "v1"}),
            data=json.dumps(self.user_details),
                            content_type="application/json"
        )

    def test_user_file_upload(self):
        response = upload_a_file()
        self.assertEqual(response.data["message"], "Successful Upload")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 
    def test_photo_no_empty_photo_field(self):
        url = reverse("file-upload",
                kwargs={"version": "v1"}
            )
        data = {"": ""}
        response = client.post(url,data,format="multipart")
        self.assertEqual(response.data[0], 'Field must not be empty')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_field_update_photo(self):
        def upload_a_file(photo=""):
            url = reverse(
                "file-upload-detail",
                kwargs={
                    "version": "v1",
                    "pk": self.user.data['id']
                }
            )
            data = {"": ""}
            return client.put(url, data, format="multipart")
        response = upload_a_file()
        self.assertEqual(response.data[0], "Field must not be empty")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_photo_update(self):
        def upload_file(photo=""):
            url = reverse(
                "file-upload-detail",
                kwargs={
                    "version": "v1",
                    "pk": self.user.data['id']
                }
            )
            image = Image.new('RGB', (100, 100))
            tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
            image.save(tmp_file)
            return client.delete(url, {"photo":tmp_file}, format="multipart")
        response = upload_file()
        self.assertEqual(response.data["message"], "Delete successful")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_user_photo(self):
        upload_a_file()
        url = reverse("file-upload-detail",
                kwargs={"version": "v1","pk": self.user.data['id']}
            )
        response = client.get(url,format="multipart")
        self.assertEqual(response.data['message'], 'Success')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_does_not_exist_when_get_request_is_made(self):
        url = reverse("file-upload-detail",
                kwargs={"version": "v1","pk": 100}
            )
        response = client.get(url,format="multipart")
        self.assertEqual(response.data['message'], 'User object not found')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_does_not_exist_when_updating(self):
        def upload_a_file(photo=""):
            url = reverse(
                "file-upload-detail",
                kwargs={
                    "version": "v1",
                    "pk": 100
                }
            )
            image = Image.new('RGB', (100, 100))
            tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
            image.save(tmp_file)

            return client.put(
                url,
                {"photo":tmp_file},
                format="multipart"       
        )
        response = upload_a_file()
        self.assertEqual(response.data['message'], 'User object not found')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
