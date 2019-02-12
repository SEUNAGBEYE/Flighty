import jwt
#
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db import models

from flighty.models import TimestampedModel

from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):

    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email' # sets email to username field to be used by `authenticate()`
    objects = UserManager()

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns user's email when an instance of a user is printed
        """
        return self.email

    def _generate_jwt_token(self):
        """
        Generates a JWT with user's id to expire in 60 days
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    @property # makes this method available via user.token
    def token(self):
        """
        Generates JWT for user
        """
        return self._generate_jwt_token()
    
    class Meta:
        db_table = 'users'

class UserProfile(TimestampedModel):
    

    user = models.OneToOneField(
        'User', on_delete=models.CASCADE
    )

    # This field is not required and it may be blank.
    image = models.ImageField(blank=True, default='default.png')

    house_address = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)

    def get_full_name(self):
        """
        Returns user's full name
        """
    
        return f'{self.first_name} {self.last_name}'.strip()

    def __str__(self):
        return self.get_full_name() or self.user.email

    class Meta:
        db_table = 'user_profiles'
