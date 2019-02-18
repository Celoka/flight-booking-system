import uuid
from django.db import models
from djmoney.models.fields import MoneyField
from django.conf import settings


# Create your models here.
class Flight(models.Model):
    """
    This model defines a Flight object
    """
    STATUS = (
        ("AVAILABLE", "Available"),
        ("ARRIVED","Arrived"),
        ("DELAYED","Delayed"),
        ("DEPARTED","Departed"),
        ("CANCELLED","Cancelled")
    )

    flight_no           = models.CharField(max_length=50, blank=True)
    scheduled_departure = models.DateTimeField(auto_now=True)
    scheduled_arrival   = models.DateTimeField(auto_now=True)
    departure_airport   = models.CharField(max_length=50, blank=True)
    arrival_airport     = models.CharField(max_length=50, blank=True)
    status              = models.CharField(choices=STATUS, max_length=50, default="AVAILABLE")
    actual_departure    = models.DateTimeField(auto_now=True)
    actual_arrival      = models.DateTimeField(auto_now=True)


class Ticket(models.Model):
    """
    Model defines a Ticket object
    """

    STATUS = (
        ("PENDING","Pending"),
        ("RESERVED","Reserved"),
        ("CONFIRMED","Confirmed"),
        ("BOOKED","Booked")
    )

    ticket_id   = models.CharField(max_length=50, blank=True)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight      = models.ForeignKey('flight_booking_app.Flight', on_delete=models.CASCADE, null=True)
    status      = models.CharField(choices=STATUS, max_length=50, default="PENDING")
    amount      = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if len(self.ticket_id.strip(" "))==0:
            self.ticket_id = generate_ticket_id()
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.ticket_id)
    
    class Meta:
        ordering = ["-created"]


def generate_ticket_id():
    return str(uuid.uuid4()).split("-")[-1]
