from datetime import datetime,timezone

from celery import shared_task
from celery.schedules import crontab
from celery.decorators import periodic_task

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Ticket
from users.models import User


@shared_task()
def ticket_notification(pk):
    """ This sends an email to user when a user books a flight ticket """
    queryset = Ticket.objects.all()
    ticket = get_object_or_404(queryset,pk=int(pk))
    if ticket:
        subject, from_email, to = 'Details of your ticket', settings.EMAIL_HOST_USER, ticket.user.email
        html_content = render_to_string('ticket_booking.html',{
            'username': ticket.user.username,
            'name': ticket.user.get_full_name(),
            'flight_number': ticket.flight.flight_number,
            'ticket_number': ticket.ticket_id,
            'depart_date': ticket.depart_date,
            'arrive_date': ticket.arrive_date,
            'departure': ticket.departure,
            'destination': ticket.destination,
            'phone_number': ticket.phone_number,
            'passport_number': ticket.passport_number,
            'contact_address': ticket.contact_address,
            'date_of_birth': ticket.date_of_birth
        })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@periodic_task(
    run_every=(crontab(hour=1, minute=0)),
    name="email_reminder_task",
    ignore_result=True
)
def user_departure_notification():
    current_datetime = datetime.now(timezone.utc)
    users = User.objects.all()
    for user in users:
        ticket = Ticket.objects.filter(user=users[0], status=Ticket.RESERVED)
        new_ticket = ticket[0]
        reserved_date = new_ticket.date_reserved
        age = current_datetime - reserved_date
        if age.days <= 1:
            subject = f'Reminder For Departure of Flight {new_ticket.flight}'
            from_email = settings.EMAIL_HOST_USER
            to = new_ticket.user.email
            html_content = render_to_string('flight_reminder.html',{
                'name': new_ticket.user.get_full_name(),
                'flight_number': new_ticket.flight,
                'depart_date': new_ticket.depart_date,
                'arrive_date': new_ticket.arrive_date,
                'departure': new_ticket.departure,
                'destination': new_ticket.destination
            })
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
  
@shared_task()
def flight_reservation(pk):
    """ This sends an email to a user when they make a flight reservation """
    queryset = Ticket.objects.all()
    flight = get_object_or_404(queryset,pk=int(pk))
    if flight:
        subject, from_email, to = 'Your flight reservation details', settings.EMAIL_HOST_USER, flight.user.email
        html_content = render_to_string('flight_reservation.html',{
            'username': flight.user.username,
            'name': flight.user.get_full_name(),
            'ticket_number': flight.ticket_id,
            'flight_status': flight.status,
            'flight_number': flight.flight.flight_number,
            'depart_date': flight.depart_date,
            'arrive_date': flight.arrive_date,
            'departure': flight.departure,
            'destination': flight.destination,
            'phone_number': flight.phone_number,
            'passport_number': flight.passport_number
        })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

@shared_task()
def flight_decline(pk):
    queryset = Ticket.objects.all()
    ticket = get_object_or_404(queryset, pk=int(pk))
    if ticket:
       subject, from_email, to = 'Your Flight Status', settings.EMAIL_HOST_USER, ticket.user.email
        html_content = render_to_string('flight_decline.html',{
            'name': ticket.user.get_full_name(),
            'flight_number': ticket.flight.flight_number
        })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()  
