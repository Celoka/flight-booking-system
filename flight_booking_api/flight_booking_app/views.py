from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets,serializers
from rest_framework.views import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import action

from .serializer import FlightSerializer,TicketSerializer
from .models import Flight,Ticket
from .permissions import IsAdminUser,IsOwner


class FlightViewSet(viewsets.ModelViewSet):
    """
    POST flight/
    GET flight/
    GET flight/:id/
    PUT flight/:id/
    DELETE flight/:id/
    """

    serializer_class = FlightSerializer
    queryset = Flight.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]
        if self.action in ('create','retrieve','destroy'):
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["POST"])
    def create_flight(self,request,version,id=None):
        data = request.data
        data._mutable = True
        data["customers"] = request.user.id
        serializer = FlightSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)


class TicketViewSet(viewsets.ModelViewSet):
    """
    POST flight/
    GET  flight/
    GET  flight/:id/
    PUT  flight/:id/
    DELETE flight/:id/
    """
    
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    lookup_field = 'id'

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]
        if self.action in ('destroy','update'):
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["POST"])
    def book(self,request,version,id=None):
        ticket = self.get_object()
        ticket_info =request.data['flight_number']
        flight_info = Flight.objects.filter(flight_number=ticket_info)
        data = request.data
        serializer = TicketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            for item in flight_info:
                item.booked=True
                item.save()
            return Response(data={
                "data": serializer.data,
                "message": "Ticket booking successful."
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)
