from django.db import models
# Create your models here.

from flighty.models import TimestampedModel

PAYMENT_CHOICES = (
    ('Cash', 'Cash'),
    ('Card', 'Card'),
)

class Ticket(TimestampedModel):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    flight = models.ForeignKey('flight.Flight', on_delete=models.CASCADE)
    is_ticketed = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)
    ticket_no = models.IntegerField(null=True)
    form_of_payment = models.CharField(max_length = 100, choices=PAYMENT_CHOICES)
    valid_till = models.DateTimeField()

    class Meta:
        db_table = 'tickets'

    def __str__(self):
        return f'User: {self.user.userprofile.get_full_name()} \n Flight: {self.flight}'