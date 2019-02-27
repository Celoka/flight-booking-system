from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token, name='create-token'),
    re_path('api/(?P<version>(v1|v2))/', include('users.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('flight_booking_app.urls'))

]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, 
  document_root=settings.MEDIA_ROOT)
