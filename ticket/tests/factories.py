import factory
from factory.django import DjangoModelFactory
from ticket.models import Ticket

class TicketFactory(DjangoModelFactory):
    class Meta:
        model = Ticket