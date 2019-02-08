
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Ticket, Passenger

@receiver(pre_save, sender=Ticket)
def update_ticket_info(sender, instance, *args, **kwargs):
    # Notice that we're checking for `created` here. We only want to do this
    # the first time the `User` instance is created. If the save that caused
    # this signal to be run was an update action, we know the user already
    # has a profile.
    instance.set_valid_till()
    instance.set_total_fare()