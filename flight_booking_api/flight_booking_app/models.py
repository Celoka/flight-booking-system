import uuid

from djmoney.models.fields import MoneyField

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _



# Create your models here.
class Flight(models.Model):
    """
    This model defines a Flight object
    """

    flight_number = models.CharField(max_length=50, blank=True,unique=True)
    depart_date = models.DateField(_(u"Depart Date"), blank=True, null=True)
    arrive_date = models.DateField(_(u"Arrive Date"), blank=True, null=True)
    departure = models.CharField(max_length=50, blank=True)
    amount = MoneyField(max_digits=14,decimal_places=2,default_currency='USD',null=True,blank=True)
    destination = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.flight_number)


class Ticket(models.Model):
    """
    Model defines a Ticket object
    """
    BOOKED = "BOOKED"
    RESERVED = "RESERVED"
    YES = "Yes"
    NO = "No"
 
    STATUS = (
        ("BOOKED","Booked"),
        ("RESERVED","Reserved")
        )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight = models.ForeignKey('flight_booking_app.Flight', on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(verbose_name='DOB')
    date_reserved = models.DateField(verbose_name='Reserved date',blank=True, null=True)
    phone_number = models.CharField(max_length=50,verbose_name='Phone')
    passport_number = models.CharField(max_length=50)
    contact_address = models.CharField(max_length=255)
    amount = MoneyField(max_digits=14,decimal_places=2,default_currency='USD',null=True,blank=True)
    depart_date = models.DateField(_(u"Depart Date"), blank=True, null=True)
    arrive_date = models.DateField(_(u"Arrive Date"), blank=True, null=True)
    departure = models.CharField(max_length=50, blank=True)
    destination = models.CharField(max_length=50, blank=True)
    status = models.CharField(choices=STATUS, max_length=50,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if len(self.ticket_id.strip(" "))==0:
            self.ticket_id = generate_ticket_id()
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.flight)


def generate_ticket_id():
    return str(uuid.uuid4()).split("-")[-1]
