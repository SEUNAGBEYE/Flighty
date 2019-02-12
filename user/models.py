import jwt
#
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

from flighty.models import TimestampedModel

class UserManager(BaseUserManager):
    """
    Manager's class for custom users
    """

    def create_user(self, email, password=None):
        """Create and return a `User` with an email, username and password."""

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Creates a super user
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):

    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email' # sets email to username field to be used by `authenticate()`
    objects = UserManager()

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
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
