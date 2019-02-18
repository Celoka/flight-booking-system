from django.urls import path
from .views import RegisterUserView

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name="auth-register")
]