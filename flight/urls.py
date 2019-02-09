from django.shortcuts import render

# Create your views here.
from django.conf.urls import url

from .views import FlightListCreate

app_name = 'flight'
urlpatterns = [
    url(r'^$', FlightListCreate.as_view()),
]