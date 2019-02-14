from datetime import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import FlightSerializer

from .models import Flight
from ticket.models import Passenger

from .permissions import IsAdminUserOrReadOnly
from flighty.response import success_response, failure_response
from flight.messages.success import FLIGHT_CREATED, FLIGHT_FETCHED, FLIGHTS_FETCHED, FLIGHT_UPDATED
from flight.messages.error import INVALID_DATE


class FlightListCreate(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = FlightSerializer

    @method_decorator(cache_page(60*60))
    def get(self, request, *args, **kwargs):
        """Gets all flights"""

        response= Flight.objects.all()
        serializer = self.serializer_class(response, many=True)
        return success_response(serializer.data, FLIGHTS_FETCHED, status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """Creates flights"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create()

        return success_response(serializer.data, FLIGHT_CREATED, status.HTTP_201_CREATED)


class FlightRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = FlightSerializer

    @method_decorator(cache_page(60*60))
    def get(self, request, *args, **kwargs):
        """Gets a single flight
        """

        data = {
            'origin': request.query_params.get('origin', ''),
            'destination': request.query_params.get('destination', ''),
            'departure_date': request.query_params.get('departureDate', '')
        }

        flight = get_object_or_404(Flight.objects.all(), pk=kwargs['id'])
        serializer = self.serializer_class(flight)

        return success_response(serializer.data, FLIGHT_FETCHED, status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """Updates a flight"""
        user_data = request.data

        flight = get_object_or_404(Flight.objects.all(), pk=kwargs['id'])
        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            flight, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(serializer.data, FLIGHT_UPDATED, status.HTTP_200_OK)


class FlightReservation(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FlightSerializer

    @method_decorator(cache_page(60*60))
    def get(self, request, *args, **kwargs):
        """Gets the reservations for a specific flight on a specific day"""

        date_string = request.query_params.get('date')

        try:
            date = datetime.strptime(date_string, '%Y-%m-%d')
        except Exception as e:
            
            error = {
                'date': [INVALID_DATE.format(date_string)]
            }

            return failure_response(error, INVALID_DATE, status.HTTP_400_BAD_REQUEST)

        flight = get_object_or_404(Flight.objects.all(), pk=kwargs['id'])


        reservations = Passenger.objects.filter(ticket__is_ticketed=True, ticket__flight_id=flight.id, ticket__created_at__date=date).count()
        available_seats = flight.travellers_capacity - reservations
        serializer = self.serializer_class(flight)
        reservations = {
            'reservations': reservations,
            'available_seats': available_seats,
            'flight': serializer.data
        }

        return success_response(reservations, '', status.HTTP_200_OK)