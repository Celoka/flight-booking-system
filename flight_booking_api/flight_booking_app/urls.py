from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import FlightViewSet,TicketViewSet


router = DefaultRouter()

router.register('ticket', TicketViewSet, base_name='tickets')
router.register('flight', FlightViewSet, base_name='flights')

urlpatterns = [
    path('', include(router.urls))
]
