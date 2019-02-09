from datetime import datetime

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


class FlightListCreate(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = FlightSerializer

    def get(self, request, *args, **kwargs):
        """Gets all flights"""

        response= Flight.objects.all()
        serializer = self.serializer_class(response, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """Creates flights"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FlightRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = FlightSerializer

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

        return Response(serializer.data, status=status.HTTP_200_OK)
    
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

        return Response(serializer.data, status=status.HTTP_200_OK)


class FlightReservation(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FlightSerializer

    def get(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.

        date_string = request.query_params.get('date')

        try:
            date = datetime.strptime(date_string, '%Y-%m-%d')
        except Exception as e:

            response = {'errors': {
                'date': [f'date={date_string} does not match this format Y-M-D']
            }}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        flight = get_object_or_404(Flight.objects.all(), pk=kwargs['id'])


        reservations = Passenger.objects.filter(ticket__is_ticketed=True, ticket__flight_id=flight.id, ticket__created_at__date=date).count()
        available_seats = flight.travellers_capacity - reservations
        serializer = self.serializer_class(flight)
        return Response({'data': {
            'reservations': reservations,
            'available_seats': available_seats,
            'flight': serializer.data
        }}, status=status.HTTP_200_OK)