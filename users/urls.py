from django.urls import path
from .views import (RegisterUserView, 
                    LoginView, 
                    ImageUploadViewSet,
                    index)

urlpatterns = [
    path('', index, name="home-route"),
    path('auth/register/', RegisterUserView.as_view(), name="auth-register"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('user/upload/', ImageUploadViewSet.as_view(), name="file-upload"),
    path('user/upload/<int:pk>/', ImageUploadViewSet.as_view(), name="file-upload-detail")
]
