from datetime import datetime


from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets,serializers,exceptions
from rest_framework.views import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import action

from .serializer import (FlightSerializer,
                        TicketSerializer)
from .tasks import (ticket_notification,
                        flight_reservation)
from .models import Flight,Ticket
from .permissions import IsAdminUser,IsOwner
from .decorators import validate_request_data


class FlightViewSet(viewsets.ModelViewSet):
    """
    POST flight/
    GET flight/
    GET flight/:pk/
    PUT flight/:pk/
    DELETE flight/:pk/
    """

    serializer_class = FlightSerializer
    queryset = Flight.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]
        if self.action in ('create','destroy','update'):
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self,request,version,pk=None):
        data = request.data
        if data['depart_date'] > data['arrive_date']:
            return Response(
                data={
                    "message":"Departure date cannot be greater than Arrival date"
                },status=status.HTTP_400_BAD_REQUEST
            )
        new_flight = dict(
           flight_number=data['flight_number'],
           depart_date=data['depart_date'],
           arrive_date=data['arrive_date'],
           departure=data['departure'],
           destination=data['destination'],
           amount=data['amount']
        )
        serializer = FlightSerializer(data=new_flight)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,version,pk=None):
        queryset = Flight.objects.all()
        data = request.data 
        if data['depart_date'] > data['arrive_date']:
            return Response(
                data={
                    "message":"Departure date cannot be greater than Arrival date"
                },status=status.HTTP_400_BAD_REQUEST
            )
        try:
            flight = get_object_or_404(queryset, pk=pk)
            serializer = FlightSerializer()
            updated_flight = serializer.update(flight, data)
            return Response(FlightSerializer(updated_flight).data,
                            status=status.HTTP_200_OK)
        except Flight.DoesNotExist:
            return Response(
                data={
                    "message": "Flight with id: {} does not exist".format(pk)
                },
                status=status.HTTP_404_NOT_FOUND)


class TicketViewSet(viewsets.ModelViewSet):
    """
    POST ticket/
    GET  ticket/
    GET  ticket/:pk/
    PUT  ticket/:pk/
    DELETE ticket/:pk/
    """
    
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]
        if self.action in ('destroy', 'update'):
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def create(self,request,version,pk=None):
        user = request.user
        data = request.data
        queryset = Flight.objects.all()
        flight = get_object_or_404(queryset, pk=data['flight'])
        ticket = Ticket.objects.filter(user=user, flight=flight)
        if ticket.exists():
            return Response(data={"A ticket already exists"},
                            status=status.HTTP_409_CONFLICT)
        if flight:
            new_ticket = dict(
                user=user.id,
                flight=flight.pk,
                date_of_birth=data['date_of_birth'],
                phone_number=data['phone_number'],
                passport_number=data['passport_number'],
                contact_address=data['contact_address'],
                depart_date=flight.depart_date,
                arrive_date=flight.arrive_date,
                departure=flight.departure,
                destination=flight.destination,
                status=Ticket.BOOKED
            )
            serializer = TicketSerializer(data=new_ticket)
            if serializer.is_valid():
                serializer.save()
                ticket_pk = serializer.data
                ticket_notification.delay(ticket_pk['id'])
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @validate_request_data
    def update(self,request,version,pk=None):
        user = request.user
        data = request.data
        queryset = Ticket.objects.all()
        ticket = get_object_or_404(queryset, pk=pk, user=user)

        if data['confirm_payment'] not in (Ticket.YES, Ticket.NO):
            msg = "Confirm payment can either be a Yes or No"
            raise exceptions.ValidationError(msg)
    
        if data['confirm_payment'] == Ticket.YES:
            if user != ticket.user:
                return Response(data={"User is not authorized to perform this operation"},
                                status=status.HTTP_401_UNAUTHORIZED)

            if ticket.status == ticket.RESERVED:
                return Response(data={"This flight has been reserved"},
                                status=status.HTTP_409_CONFLICT)
            try:
                flight = Flight.objects.get(pk=data['flight_pk'])
                new_data = dict(
                    amount=flight.amount,
                    date_reserved=datetime.now(),
                    status=Ticket.RESERVED
                )
                serializer = TicketSerializer()
                updated_ticket = serializer.update(ticket,new_data)
                flight_reservation.delay(pk)
                return Response(TicketSerializer(updated_ticket).data,
                            status=status.HTTP_200_OK)
            except Flight.DoesNotExist:
                return Response(
                    data={"message":"Flight object not found"},
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data={
                "message": "Confirmation declined"
            },status=status.HTTP_200_OK)
