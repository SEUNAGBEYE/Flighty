from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import FlightSerializer

from .models import Flight

from .permissions import IsAdminUserOrReadOnly


class FlightListCreate(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = FlightSerializer

    def get(self, request, *args, **kwargs):
        """Gets all flights"""
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.

        response= Flight.objects.all()
        serializer = self.serializer_class(response, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """Creates flights"""

        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
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

        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.

        data = {
            'origin': request.query_params.get('origin', ''),
            'destination': request.query_params.get('destination', ''),
            'departure_date': request.query_params.get('departureDate', '')
        }

        flight = get_object_or_404(Flight.objects.all(), pk=kwargs['id'])
        serializer = self.serializer_class(flight)

        return Response(serializer.data, status=status.HTTP_200_OK)