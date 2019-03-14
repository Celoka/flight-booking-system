import json

from django.urls import reverse
from django.shortcuts import get_object_or_404

from rest_framework.views import status
from rest_framework.test import APIClient,APITestCase

from users.models import User

from flight_booking_app.models import Flight, Ticket
from flight_booking_app.serializer import TicketSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_a_ticket(user,flight,ticket_id,date_of_birth,date_reserved,
                        phone_number,passport_number,contact_address,depart_date,
                        arrive_date,departure,destination):
        """
        Create a Ticket in the db
        """
        Ticket.objects.create(
            user=user,
            flight=flight,
            ticket_id=ticket_id,
            date_of_birth=date_of_birth,
            date_reserved=date_reserved,
            phone_number=phone_number,
            passport_number=passport_number,
            contact_address=contact_address,
            depart_date=depart_date,
            arrive_date=arrive_date,
            departure=departure,
            destination=destination
        )
    
    def login(self, username, password):
        # get a token from DRF
        response = self.client.post(
            reverse("create-token"),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token
    
    def make_a_request(self,kind="post", **kwargs):
        if kind == "post":
            return self.client.post(
                reverse(
                    "ticket",
                    kwargs={
                        "version": kwargs["version"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        elif kind == "put":
            return self.client.put(
                reverse(
                    "flight-detail",
                    kwargs={
                        "version": kwargs["version"],
                        "pk": kwargs["id"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        else:
            return None

    def setUp(self):

        # create a user
        self.user_1 = User.objects.create_user(
            username="User",
            email="user@mail.com",
            password="testing",
            first_name="test",
            last_name="user",  
        )
        self.user_2 = User.objects.create_user(
            username="User Test",
            email="test.mail@mail.com",
            password="testing",
            first_name="test",
            last_name="user",  
        )
        self.flight = Flight.objects.create(
            flight_number="Fx-ggfg",
            depart_date="2018-02-13",
            arrive_date="2018-02-14",
            departure="Lagos",
            destination="London",
            amount=100)
        self.flight = Flight.objects.get(pk=self.flight.pk)
        user = User.objects.get(pk=self.user_1.pk)
        self.ticket = Ticket.objects.create(
            user=user,
            flight=self.flight,
            ticket_id="75753",
            date_of_birth="1960-02-13",
            date_reserved="2018-03-13",
            phone_number="0908856744",
            passport_number="NGN-465hhf",
            contact_address="West Indies",
            depart_date=self.flight.depart_date,
            arrive_date=self.flight.arrive_date,
            departure=self.flight.departure,
            destination=self.flight.destination
        )

class AllTicketTest(BaseViewTest):

    def test_get_all_tickets(self):
        """
        This test ensures that all tickets added in the setup
        methods exist when we make a GET request to the ticket/ endpoint
        """
        self.login('User', 'testing')
        response = self.client.get(
            reverse('ticket-list', kwargs={"version": "v1"})
        )
        expected = Ticket.objects.all()
        serialized = TicketSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_a_single_ticket(self):
        """
        This test ensures that a single ticket is retrieved 
        when we make a GET request to the ticket/ endpoint
        """
        self.login('User', 'testing')
        response = self.client.get(
            reverse("ticket-detail",kwargs={"version": "v1", "pk": self.ticket.pk})
        )
        queryset = Ticket.objects.all()
        expected = get_object_or_404(queryset, pk=self.ticket.pk)
        serialized = TicketSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_create_ticket(self):
        ticket_details = dict(
            flight=self.flight.pk,
            date_of_birth="1960-02-13",
            date_reserved="2018-03-13",
            phone_number="0908856744",
            passport_number="NGN-465hhf",
            contact_address="West Indies",
            depart_date="2018-02-13",
            arrive_date="2018-02-14",
            departure="Lagos",
            destination="London"
        )
        self.login("User Test", 'testing')
        url = reverse('ticket-list', kwargs={"version": "v1"})
        response = self.client.post(url, data=json.dumps(ticket_details), 
                                content_type='application/json')
        self.assertEqual(response.data["date_of_birth"],"1960-02-13")
        self.assertEqual(response.data["phone_number"],"0908856744")
        self.assertEqual(response.data["passport_number"],"NGN-465hhf")
        self.assertEqual(response.data["status"],"BOOKED")
        self.assertEqual(response.data["departure"],"Lagos")
        self.assertEqual(response.data["destination"],"London")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_ticket_already_exist(self):
        ticket_details = dict(
            flight=self.flight.pk,
            date_of_birth="1960-02-13",
            date_reserved="2018-03-13",
            phone_number="0908856744",
            passport_number="NGN-465hhf",
            contact_address="West Indies",
            depart_date="2018-02-13",
            arrive_date="2018-02-14",
            departure="Lagos",
            destination="London"
        )
        self.login("User", 'testing')
        url = reverse('ticket-list', kwargs={"version": "v1"})
        response = self.client.post(url, data=json.dumps(ticket_details), 
                                content_type='application/json')
        self.assertEqual(response.data['message'], 'A ticket already exists')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_user_make_flight_reservation(self):
        confirmation_detail = dict(
            confirm_payment="Yes"
        )
        self.login("User", 'testing')
        url = reverse('ticket-detail', 
                kwargs={
                    "version":"v1",
                    "pk": self.ticket.pk})        
        response = self.client.put(url, data=json.dumps(confirmation_detail),
                                content_type='application/json')
        self.assertEqual(response.data['ticket_id'], '75753')
        self.assertEqual(response.data['date_of_birth'], '1960-02-13')
        self.assertEqual(response.data['phone_number'], '0908856744')
        self.assertEqual(response.data['passport_number'], 'NGN-465hhf')
        self.assertEqual(response.data['contact_address'], 'West Indies')
        self.assertEqual(response.data['depart_date'], '2018-02-13')
        self.assertEqual(response.data['arrive_date'], '2018-02-14')
        self.assertEqual(response.data['departure'], 'Lagos')
        self.assertEqual(response.data['destination'], 'London')
        self.assertEqual(response.data['status'], 'RESERVED')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test user flight reservation already exist
        self.login("User", 'testing')
        url = reverse('ticket-detail', 
                kwargs={
                    "version":"v1",
                    "pk": self.ticket.pk})        
        response = self.client.put(url, data=json.dumps(confirmation_detail),
                                content_type='application/json')
        self.assertEqual(response.data['message'], 'This flight has been reserved')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_user_decline_flight_reservation(self):
        confirmation_detail = dict(
            confirm_payment="No"
        )
        self.login("User", 'testing')
        url = reverse('ticket-detail', 
                kwargs={
                    "version":"v1",
                    "pk": self.ticket.pk})        
        response = self.client.put(url, data=json.dumps(confirmation_detail),
                                content_type='application/json')
        self.assertEqual(response.data['message'], 'Confirmation declined')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
