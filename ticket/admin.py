
from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Ticket, Passenger

class TicketAdmin(admin.ModelAdmin):
    pass

class PassengerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Passenger, PassengerAdmin)