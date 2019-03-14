from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import FlightViewSet,TicketViewSet


router = DefaultRouter()

router.register('ticket', TicketViewSet)
router.register('flight', FlightViewSet)

urlpatterns = [
    path('', include(router.urls))
]
