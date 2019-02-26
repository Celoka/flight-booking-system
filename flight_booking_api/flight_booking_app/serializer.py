from rest_framework import serializers

from .models import Flight, Ticket


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        extra_kwargs = {'password': {'read_only': True}}
        fields = (
            'id',
            'flight',
            'ticket_id',
            'date_of_birth',
            'phone',
            'passport_number',
            'contact_address',
        )
