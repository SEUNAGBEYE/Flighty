from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .serializers import TicketSerializer

from .models import Ticket

from .permissions import TicketPermission
from .renderers import TicketJSONRenderer

from .tasks import send_e_ticket


class TicketListCreate(APIView):
    permission_classes = (TicketPermission,)
    serializer_class = TicketSerializer
    renderer_classes = (TicketJSONRenderer, )

    def get(self, request, *args, **kwargs):
        """Gets the current user tickets

        If the current user is an admin, it gets all the tickets in the databse
        """

        response = Ticket.objects.filter(user__pk=request.user.id)
        serializer = self.serializer_class(response, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """Purchases or Books a ticket"""

        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        _, created = serializer.create()
        if created:
            send_e_ticket.delay(serializer.data, request.user.email, 'Your E Ticket')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TicketRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (TicketPermission,)
    serializer_class = TicketSerializer

    def get(self, request, *args, **kwargs):
        """Gets a single ticket"""

        ticket = get_object_or_404(Ticket.objects.all(), pk=kwargs['id'])
        serializer = self.serializer_class(ticket)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Updates a ticket information"""

        ticket = get_object_or_404(Ticket.objects.all(), pk=kwargs['id'])
        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            ticket, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
