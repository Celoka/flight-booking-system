import pytz
from datetime import datetime

from rest_framework.views import status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import APIException

def validate_request_data(fn):
    def decorated(*args, **kwargs):
        confirm_payment=args[0].request.data.get("confirm_payment")
        if confirm_payment =="":
            return Response(
                data={
                    "message": "Confirm Payment field cannot be empty"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated

def convert_date(date):
    new_date = date.split('-')
    try:
        year = int(new_date[0])
        month = int(new_date[1])
        day = int(new_date[2])
        search_date = datetime(year=year, month=month, 
                                day=day, hour=0, 
                                minute=0, second=0).replace(tzinfo=pytz.UTC)
        return search_date
    except:
        raise APIException(detail="The date provided is not the correct format")

