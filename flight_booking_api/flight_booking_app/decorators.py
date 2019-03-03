from rest_framework.views import status
from rest_framework.response import Response
from rest_framework import serializers

def validate_request_data(fn):
    def decorated(*args, **kwargs):

        flight_pk=args[0].request.data.get("flight_pk")
        confirm_payment=args[0].request.data.get("confirm_payment")
        if flight_pk =="" or confirm_payment =="":
            return Response(
                data={
                    "message": "Fields cannot be empty"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated
