from django.urls import path
from .views import (RegisterUserView, 
                    LoginView, 
                    ImageUploadViewSet)

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name="auth-register"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('user/upload/', ImageUploadViewSet.as_view(), name="file-upload")
]
