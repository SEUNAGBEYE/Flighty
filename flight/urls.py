from django.shortcuts import render

# Create your views here.
from django.conf.urls import url

from .views import (
    FlightListCreate,
    FlightRetrieveUpdateDestroyAPIView,
    FlightReservation
)

app_name = 'flight'
urlpatterns = [
    url(r'^$', FlightListCreate.as_view(), name='flight-create-list'),
    url(r'^(?P<id>\d+)$', FlightRetrieveUpdateDestroyAPIView.as_view(), name='flight-retrieve-update'),
    url(r'^(?P<id>\d+)/reservations', FlightReservation.as_view(), name='flight-reservations'),
]