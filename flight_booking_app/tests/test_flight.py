import json

from django.urls import reverse
from django.shortcuts import get_object_or_404


from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from users.models import User

from flight_booking_app.models import Flight,Ticket
from flight_booking_app.serializer import (FlightSerializer,
                                            TicketSerializer)


# tests for models

class FlightModelTest(APITestCase):
    def setUp(self):
        self.a_flight = Flight.objects.create(
            flight_number="Fx-ggfg",
            depart_date="2018-02-13",
            arrive_date="2018-02-14",
            departure="Lagos",
            destination="London",
            amount=100)

    def test_a_flight(self):
        self.assertEqual(self.a_flight.flight_number, "Fx-ggfg")
        self.assertEqual(self.a_flight.depart_date, "2018-02-13")
        self.assertEqual(self.a_flight.arrive_date, "2018-02-14")
        self.assertEqual(self.a_flight.departure, "Lagos")
        self.assertEqual(self.a_flight.destination, "London")

class TicketModelTest(APITestCase):
    def setUp(self):
        self.a_flight = Flight.objects.create(
            flight_number="Fx-ggfg",
            depart_date="2018-02-13",
            arrive_date="2018-02-14",
            departure="Lagos",
            destination="London",
            amount=100)
        self.a_user = User.objects.create(
            username="West",
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            password="EUROCKF$1"
        )
        flight = Flight.objects.get(pk=self.a_flight.pk)
        user = User.objects.get(pk=self.a_user.pk)
        self.a_ticket = Ticket.objects.create(
            user=user,
            flight=flight,
            ticket_id="75753",
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
    def test_a_ticket(self):
        self.assertEqual(self.a_ticket.flight.flight_number, 'Fx-ggfg')
        self.assertEqual(self.a_ticket.ticket_id, "75753")
        self.assertEqual(self.a_ticket.date_of_birth, "1960-02-13")
        self.assertEqual(self.a_ticket.date_reserved, "2018-03-13")
        self.assertEqual(self.a_ticket.phone_number, "0908856744")
        self.assertEqual(self.a_ticket.passport_number, "NGN-465hhf")
        self.assertEqual(self.a_ticket.contact_address, "West Indies")
        self.assertEqual(self.a_ticket.departure, "Lagos")
        self.assertEqual(self.a_ticket.destination, "London")
        self.assertEqual(self.a_ticket.depart_date, "2018-02-13")
        self.assertEqual(self.a_ticket.arrive_date, "2018-02-14")


# test for views

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_a_flight(flight_number, depart_date,arrive_date,
                        departure,destination, amount):
        """
        Create a Flight in the db
        """
        Flight.objects.create(
            flight_number=flight_number,
            depart_date=depart_date,
            arrive_date=arrive_date,
            departure=departure,
            destination=destination,
            amount=amount)
    
    def login_client(self, username="", password=""):
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

    def setUp(self):

        # create a admin user
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
            is_staff=True
        )
        self.create_a_flight('Fx-77j','2018-02-13',
                        '2018-02-14','Lagos','London',100)
        self.create_a_flight('Fx-88v','2018-02-13',
                        '2018-02-14','Lagos','London',500)

        self.valid_flight_id = 5
        self.invalid_flight_id = 100


class GetASingleFlightTest(BaseViewTest):

    def test_get_a_flight(self):
        """
        This test ensures that a single flight of a given id is
        returned
        """
        self.login_client('test_user', 'testing')
        
        response = self.client.get(
             reverse("flight-detail",kwargs={"version": "v1", "pk": self.valid_flight_id})
        )
        flight = Flight.objects.get(flight_number='Fx-88v')
        serialized = FlightSerializer(flight)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test with a flight that does not exist
        response = self.client.get(
             reverse("flight-detail",kwargs={"version": "v1", "pk": self.invalid_flight_id})
        )
        self.assertEqual(
            response.data['detail'],
           'Not found.'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class GetAllFlightTest(BaseViewTest):

    def test_admin_create_flight(self):
        flight_details = dict(
            flight_number="787-yyT",
            depart_date="2018-02-13",
            arrive_date="2018-02-14",
            departure="Lagos",
            destination="London",
            amount=100)
        self.login_client('test_user', 'testing')
        url = reverse('flight-list', kwargs={"version": "v1"})
        response = self.client.post(url, data=json.dumps(flight_details), 
                                content_type='application/json')
        self.assertEqual(response.data["flight_number"],"787-yyT")
        self.assertEqual(response.data["depart_date"],"2018-02-13")
        self.assertEqual(response.data["arrive_date"],"2018-02-14")
        self.assertEqual(response.data["departure"],"Lagos")
        self.assertEqual(response.data["destination"],"London")
        self.assertEqual(response.data["amount"],'100.00')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_flights(self):
        """
        This test ensures that all flights added in the setUp method
        exist when we make a GET request to the flight/ endpoint
        """
        self.login_client('test_user', 'testing')
        response = self.client.get(
            reverse('flight-list', kwargs={"version": "v1"})
        )
        expected = Flight.objects.all()
        serialized = FlightSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_a_flight(self):
        """
        This test ensures that a single flight can be updated.
        """
        self.login_client('test_user', 'testing')
        flight_details = dict(
            flight_number="FX-JJP",
            depart_date="2018-02-13",
            arrive_date="2018-02-14",
            departure="USA",
            destination="London",
            amount=100)
        url = reverse('flight-detail', 
                kwargs={
                    "version":"v1",
                    "pk":3}) 
        response = self.client.put(url, data=json.dumps(flight_details),
                                   content_type='application/json')


class DeleteAflightTest(BaseViewTest):

    def test_delete_a_flight(self):
        """
        This test ensures that a single flight of a given id is
        returned
        """
        self.login_client('test_user', 'testing')
        response = self.client.delete(
            reverse("flight-detail",kwargs={"version": "v1", "pk": 2})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # test with invalid data
        response = self.client.delete(
             reverse("flight-detail",kwargs={"version": "v1", "pk": self.invalid_flight_id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
