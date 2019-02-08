from django.conf.urls import url

from .views import FlightRetrieveUpdateDestroyAPIView, FlightListCreate, FlightReservation


app_name = 'flight'
urlpatterns = [
    url(r'^(?P<id>\d+)$', FlightRetrieveUpdateDestroyAPIView.as_view()),
    url(r'^(?P<id>\d+)/reservations', FlightReservation.as_view()),
    url(r'^$', FlightListCreate.as_view()),
]