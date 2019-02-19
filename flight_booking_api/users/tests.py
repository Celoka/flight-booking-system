import json
from django.urls import reverse

# Create your tests here.
from rest_framework.test import APIClient,APITestCase
from rest_framework.views import status
from .models import User

class BaseViewTest(APITestCase):
    client = APIClient()

    def register_a_user(self,first_name="",last_name="",email="",password=""):
        return self.client.post(
            reverse(
                "auth-register",
                kwargs={
                    "version": "v1"
                }
            ),
            data=json.dumps(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": password
                }
            ),
            content_type='application/json'
        )
    
    def login_a_user(self, email="",password=""):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        return self.client.post(
            url,
            data=json.dumps({
                "email": email,
                "password": password
            }),
            content_type="application/json"
        )


class RegisterUserTest(BaseViewTest):
    """
    Tests for auth/register/endpoint
    """
    def test_register_a_user(self):
        response = self.register_a_user("admin","user","test@email.com","test_admin")
        self.assertEqual(response.data["first_name"],"admin")
        self.assertEqual(response.data["last_name"],"user")
        self.assertEqual(response.data["email"],"test@email.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test a user with invalid credentials
        response = self.register_a_user()

        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        self.register_a_user("admin","user","test@email.com","test_admin")
        response = self.login_a_user("test@email.com", "test_admin")
        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test a user with invalid login credentials
        response = self.login_a_user("anonymous", "pass")

        # assert status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
