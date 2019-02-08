from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .serializers import TicketSerializer

from .models import Ticket

from .permissions import TicketPermission
from flighty.renderers import FlightyJSONRenderer
from .renderers import TicketJSONRenderer

class TicketRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (TicketPermission,)
    serializer_class = TicketSerializer

    def get(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.

        ticket = get_object_or_404(Ticket.objects.all(), pk=kwargs['id'])
        serializer = self.serializer_class(ticket)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        ticket = get_object_or_404(Ticket.objects.all(), pk=kwargs['id'])
        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            flight, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketListCreate(APIView):
    permission_classes = (TicketPermission,)
    serializer_class = TicketSerializer
    renderer_classes = (TicketJSONRenderer, )

    def get(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.

        response= Ticket.objects.filter(user__pk=request.user.id)
        serializer = self.serializer_class(response, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.create()

        return Response(serializer.data, status=status.HTTP_201_CREATED)