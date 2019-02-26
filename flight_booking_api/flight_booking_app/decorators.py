
import re

from rest_framework.views import status

from rest_framework.response import Response
from rest_framework import serializers

from .models import Flight


def validate_request_data(fn):
    def decorated(*args, **kwargs):
    
        flight_no=args[0].request.data.get("flight_no")
        departure_time=args[0].request.data.get("departure_time")
        arrival_time=args[0].request.data.get("arrival_time")
        departure_airport=args[0].request.data.get("departure_airport")
        arrival_airport=args[0].request.data.get("arrival_airport")
        arrival_date=args[0].request.data.get("arrival_date")
        departure_date=args[0].request.data.get("departure_date")
        flight_status=args[0].request.data.get("flight_status").replace(" ","")

        AVAILABLE_STATUS = ("AVAILABLE","DEPARTED","DELAYED","CANCELLED","LANDED","ARRIVED")

        if Flight.objects.filter(flight_no=flight_no).exists():
            return Response(
                data={
                    "message":  "This flight already exists"
                },
                status=status.HTTP_409_CONFLICT)

        if flight_status not in AVAILABLE_STATUS:
            return Response(
                data={
                    "message": "Status must be any of the following AVAILABLE,DEPARTED,DELAYED,CANCELLED,LANDED,ARRIVED"
                },
                status=status.HTTP_400_BAD_REQUEST)

        if flight_no =="" or departure_time ==""\
            or arrival_time == "" or departure_airport==""\
                or arrival_airport =="" or arrival_date==""\
                    or departure_date =="" or flight_status=="":
            return Response(
                data={
                    "message": "All the fields are required to register a flight"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated

