from django.urls import path
from .views import RegisterUserView, LoginView

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name="auth-register"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
]
