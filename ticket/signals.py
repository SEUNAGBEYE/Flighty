from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Ticket

@receiver(pre_save, sender=Ticket)
def update_ticket_info(sender, instance, *args, **kwargs):
    """Calculates ticket fare and validity before saving"""
    instance.set_valid_till()
    instance.set_total_fare()

