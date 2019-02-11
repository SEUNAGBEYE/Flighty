import factory
from factory.django import DjangoModelFactory
from flight.models import Flight

class FlightFactory(DjangoModelFactory):
    class Meta:
        model = Flight