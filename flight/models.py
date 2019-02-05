from django.db import models

# Create your models here.

from flighty.models import TimestampedModel

class Flight(TimestampedModel):
    travel_date = models.DateTimeField()
    travelling_from = models.CharField(max_length = 100)
    travelling_to = models.CharField(max_length = 100)
    airline_code = models.CharField(max_length = 100)
    status = models.CharField(max_length = 100)
    fare = models.FloatField(default=float(0.00))

    def __str__(self):
        return f"""
        Dest: {self.travelling_from} to {self.travelling_to}\n
        Date: {self.travel_date}\n
        Airline: {self.airline_code}
        """
    
    class Meta:
        db_table = 'flights'

