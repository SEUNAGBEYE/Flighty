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
    url(r'^$', FlightListCreate.as_view()),
    url(r'^(?P<id>\d+)$', FlightRetrieveUpdateDestroyAPIView.as_view()),
    url(r'^(?P<id>\d+)/reservations', FlightReservation.as_view()),
]