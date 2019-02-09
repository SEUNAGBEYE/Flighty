from django.db import models

# Create your models here.

from flighty.models import TimestampedModel

status_choices = (
    ('scheduled', 'Scheduled'),
    ('delayed', 'Delayed'),
    ('departed', 'Departed'),
    ('in_air', 'In Air'),
    ('expected', 'Expected'),
    ('diverted', 'Diverted'),
    ('recovery', 'Recovery'),
    ('landed', 'Landed'),
    ('arrived', 'Arrived'),
    ('cancelled', 'Cancelled'),
    ('no_take_off_info_contact_airline', 'No Take off Info Contact Airline'),
    ('past_flight', 'Past flight')
)

flight_class = (
    ('economy', 'Economy'),
    ('premium', 'Premium'),
    ('business', 'Business'),
    ('first_class', 'First Class')
)

class Flight(TimestampedModel):
    departure_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True)
    origin = models.CharField(max_length = 100)
    destination = models.CharField(max_length = 100)
    airline_code = models.CharField(max_length = 100)
    status = models.CharField(max_length = 100, choices=status_choices)
    fare = models.FloatField(default=float(0.00))
    one_way = models.BooleanField(default=True)
    stops = models.IntegerField(default=0)
    flight_class = models.CharField(max_length = 100, choices=flight_class, default='economy')
    travellers_capacity = models.IntegerField(default=100)

    def __str__(self):
        return f"""
        Dest: {self.origin} to {self.destination}\n
        Date: {self.departure_date}\n
        Airline: {self.airline_code}
        """
    
    class Meta:
        db_table = 'flights'