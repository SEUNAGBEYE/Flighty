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
    
    def post(self, request, *args, **kwargs):
        """Creates flights"""

        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create()

        return Response(serializer.data, status=status.HTTP_201_CREATED)