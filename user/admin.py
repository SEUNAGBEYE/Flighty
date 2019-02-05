from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import User, UserProfile

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserProfile, UserProfileAdmin)
