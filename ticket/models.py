from datetime import datetime, timedelta
from django.db import models
# Create your models here.

from flighty.models import TimestampedModel

PAYMENT_CHOICES = (
    ('Cash', 'Cash'),
    ('Card', 'Card'),
    ('None', 'Not paid'),
)

class Ticket(TimestampedModel):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    flight = models.ForeignKey('flight.Flight', on_delete=models.CASCADE)
    is_ticketed = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)
    ticket_no = models.IntegerField(null=True)
    form_of_payment = models.CharField(max_length = 100, choices=PAYMENT_CHOICES)
    valid_till = models.DateTimeField()
    total_fare  = models.FloatField(max_length = 100, default=0)
    number_of_travellers = models.IntegerField(default=1)


    def generate_ticket_no(self):
        pass
    
    def set_valid_till(self):
        valid_till = datetime.now() + timedelta(weeks=12)
        self.valid_till = valid_till
        return valid_till
    
    def set_total_fare(self):
        total_fare = self.number_of_travellers * self.flight.fare
        self.total_fare = total_fare
        return total_fare

    class Meta:
        db_table = 'tickets'

    def __str__(self):
        return f'User: {self.user.email} \n Flight: {self.flight}'


class Passenger(TimestampedModel):
    
    name  = models.CharField(max_length = 100)

    # In addition to the `bio` field, each user may have a profile image or
    # avatar. This field is not required and it may be blank.
    email = models.EmailField(blank=True)
    ticket = models.ForeignKey('ticket.Ticket', on_delete=models.CASCADE, related_name='passengers')
    nationality = models.CharField(max_length=100)
    passport_no = models.CharField(max_length=100)
    expiration_date = models.DateField()
    issuarance_country = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'passengers'


