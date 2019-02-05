from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Ticket

class TicketAdmin(admin.ModelAdmin):
    pass
admin.site.register(Ticket, TicketAdmin)