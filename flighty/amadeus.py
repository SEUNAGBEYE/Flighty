from os import environ

from amadeus import Client

amadeus = Client(
    client_id=environ['AMADEUS_API_KEY'],
    client_secret=['AMADEUS_SECRET_KEY']
)