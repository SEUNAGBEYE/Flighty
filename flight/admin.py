from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Flight

class FlightAdmin(admin.ModelAdmin):
    pass
admin.site.register(Flight, FlightAdmin)