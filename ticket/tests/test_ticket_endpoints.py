import json
from datetime import datetime, timedelta
from unittest.mock import patch

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from user.tests.factories import UserFactory
from flight.tests.factories import FlightFactory
from ticket.tests.factories import TicketFactory
from ticket.models import Ticket, Passenger
from ticket.messages.success import TICKET_CREATED
from ticket.serializers import TicketSerializer


class TestFlightEndpoint(APITestCase):

    def _auth_header(self, token):
        return f'Bearer {token}'

    def _login(self, data):
        url = reverse('user:signin')
        return self.client.post(url, data, format='json')

    def setUp(self):
        password = 'password'
        self.admin = UserFactory(
            is_staff=True,
            email='admin@test.com',
            password=password
        )
        self.user = UserFactory(
            email='user@test.com',
            password=password
        )
        
        admin_token = self._login(dict(email=self.admin.email, password=password)).data['data']['token']
        
        self._admin_header = self._auth_header(admin_token)

        token = self._login(dict(email=self.user.email, password=password)).data['data']['token']

        self._header = self._auth_header(token)
        
        self.flight_data_two = {
            'departure_date': datetime.now() + timedelta(weeks=2),
            'return_date': datetime.now() + timedelta(weeks=4),
            'destination': 'BAC',
            'origin': 'SAN',
            'airline_code': 'B435',
            'fare': 350000,
            'one_way': True,
            'stops': 2,
            'flight_class': 'economy',
            'status': 'scheduled',
            'travellers_capacity': 100
        }

        self.flight = FlightFactory(**self.flight_data_two)

        self.ticket_data = {
            'form_of_payment': 'Cash',
            'passengers': [{
                'name': 'Passenger 1',
                'email': 'passenger@test.com',
                'nationality': 'Nigeria',
                'issuarance_country': 'Nigeria',
                'passport_no': 'AWERTY6UIJ',
                'expiration_date': '2030-02-02',
                'telephone': '1234567890',
            }],
            'flight_id': self.flight.id
        }

        self.ticket_data_two = {
            'form_of_payment': 'Card',
            'passengers': [{
                'name': 'Passenger 1',
                'email': 'passenger@test.com',
                'nationality': 'Nigeria',
                'issuarance_country': 'Nigeria',
                'passport_no': 'AWERTY6UIJ',
                'expiration_date': '2030-02-02',
                'telephone': '1234567890',
            }],
            'flight_id': self.flight.id
        }

        serializer = TicketSerializer(data=self.ticket_data_two, context={'user': self.admin})
        serializer.is_valid(raise_exception=True)
        self.ticket = serializer.create()[0]

        self.invalid_ticket_data = {
            'form_of_payment': 'Money',
            'passengers': [{}],
            'flight_id': self.flight.id
        }


    # @patch('ticket.tasks.send_e_ticket')
    # @patch('ticket.tasks.email')
    # def test_create_ticket_with_valid_data_succeeds(self, email, send_e_ticket):
    #     url = reverse('ticket:ticket-create-list')
    #     response = self.client.post(url, 
    #     self.ticket_data, format='json', HTTP_AUTHORIZATION=self._admin_header)
    #     response_data = response.data
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response_data['message'], TICKET_CREATED)
    #     self.assertEqual(response_data['data']['form_of_payment'], self.ticket_data['form_of_payment'])
    #     self.assertEqual(response_data['data']['flight']['id'], self.ticket_data['flight_id'])
    #     assert 'passengers' in response_data['data']
    #     assert response_data['data']['form_of_payment'].startswith(self.ticket_data['form_of_payment'])
    #     assert send_e_ticket.assert_called
    #     assert email.assert_called

    def test_create_ticket_with_invalid_data_fails(self):
        url = reverse('ticket:ticket-create-list')
        response = self.client.post(url, 
        self.invalid_ticket_data, format='json', HTTP_AUTHORIZATION=self._admin_header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert 'passengers' in response_data['errors']
        payment_error = f'"{self.invalid_ticket_data["form_of_payment"]}" is not one'
        assert response_data['errors']['form_of_payment'][0].startswith(payment_error)


    def test_get_user_tickets_succeeds(self):
        url = reverse('ticket:ticket-create-list')

        response = self.client.get(url, HTTP_AUTHORIZATION=self._admin_header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response_data['data']) == 1

    def test_get_a_ticket_succeeds(self):
        url = reverse('ticket:ticket-retrieve-update', kwargs=dict(id=self.ticket.id))

        response = self.client.get(url, HTTP_AUTHORIZATION=self._admin_header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['data']['id'], self.flight.id)
        self.assertEqual(response_data['data']['form_of_payment'], self.ticket_data_two['form_of_payment'])
        self.assertEqual(response_data['data']['flight']['id'], self.ticket_data_two['flight_id'])

    def test_get_a_ticket_with_wrong_id_fails(self):
        url = reverse('ticket:ticket-retrieve-update', kwargs=dict(id=100))

        response = self.client.get(url, HTTP_AUTHORIZATION=self._admin_header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data['detail'], 'Not found.')
    
    def test_update_ticket_with_valid_data_succeeds(self):
        url = reverse('ticket:ticket-retrieve-update', kwargs=dict(id=self.ticket.id))

        ticket_data = self.ticket_data_two.copy()
        ticket_data['form_of_payment'] = 'Cash'

        response = self.client.patch(url, 
        ticket_data, format='json', HTTP_AUTHORIZATION=self._admin_header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['data']['form_of_payment'], ticket_data['form_of_payment'])
        self.assertEqual(response_data['data']['flight']['id'], ticket_data['flight_id'])
        assert len(Ticket.objects.all()) == 1

    def test_update_ticket_with_wrong_id_fails(self):
        url = reverse('ticket:ticket-retrieve-update', kwargs=dict(id=100))

        response = self.client.patch(url, 
        self.ticket_data, format='json', HTTP_AUTHORIZATION=self._admin_header)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data['detail'], 'Not found.')