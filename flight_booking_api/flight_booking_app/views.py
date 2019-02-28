from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets,serializers
from rest_framework.views import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import action

from .serializer import (FlightSerializer,
                        TicketSerializer)
from .models import Flight,Ticket
from .permissions import IsAdminUser,IsOwner


class FlightViewSet(viewsets.ModelViewSet):
    """
    POST flight/:userId/create_flight
    GET flight/
    GET flight/:flight_id/
    PUT flight/:flight_id/
    DELETE flight/:flight_id/
    """

    serializer_class = FlightSerializer
    queryset = Flight.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]
        if self.action in ('create','retrieve','destroy'):
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["POST"])
    def create_flight(self,request,version,pk=None):
        data = request.data
        flight = Flight.objects.filter(flight_number=data['flight_number']).exists()
        if flight:
            return Response(data={
                "error": "Flight has already been created"
            },
            status=status.HTTP_409_CONFLICT)
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
    POST ticket/:user_id/book
    GET  ticket/
    GET  ticket/:ticket_id/
    PUT  ticket/:user_id/buy_ticket
    DELETE ticket/:ticket_id/
    """
    
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]
        if self.action in ('destroy', 'update'):
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["POST"])
    def book(self,request,version,pk=None):
        ticket_info =request.data['flight_number']
        flight_info = Flight.objects.filter(flight_number=ticket_info)
        if not flight_info:
            return Response(data={
                    "error":"Flight not found"},
                    status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = TicketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            for item in flight_info:
                if item.flight_status == "Pending":
                    item.flight_status = Flight.BOOKED
                    item.save()
                else:
                    return Response(data={
                    "error":"This flight has either been booked or reserved"},
                    status=status.HTTP_403_FORBIDDEN)
            return Response(data={
                "message":"Ticket booking successful",
                "data": serializer.data
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=["PUT"])
    def buy_ticket(self, request, version, pk=None):
        data = request.data
        try:
            ticket = Ticket.objects.filter(ticket_id=data['ticket_id'])
        except Ticket.DoesNotExist as e:
            return Response(
                data={"error":"Ticket object not found"},
                status=status.HTTP_404_NOT_FOUND)
        flight_info = Flight.objects.filter(flight_number=data['flight_number'])
        for item in flight_info:
            if item.amount is None:
                flight_id = item.pk
                item.amount = data['amount']
                item.flight_status = Flight.RESERVED
                item.save()
            else:
                return Response(data={
                    "error":"This flight ticket has been purchased"},
                    status=status.HTTP_403_FORBIDDEN)
        return Response(data={
                "message": "Ticket booking successful",
                "data": {
                "flight_id": flight_id,
                "flight_number": data["flight_number"],
                "amount": data["amount"],
                "ticket_id":data["ticket_id"]
                }
            },status=status.HTTP_201_CREATED)
