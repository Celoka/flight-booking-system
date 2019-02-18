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
