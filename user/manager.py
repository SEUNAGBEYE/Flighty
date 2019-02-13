"""
User Manager module:
Reference : https://thinkster.io/tutorials/django-json-api/authentication
"""

from django.contrib.auth.models import BaseUserManager

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