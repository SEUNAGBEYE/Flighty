"""JWT Authentication module

Raises:
    exceptions.AuthenticationFailed: Raise this exception when authentication failed

Reference : https://thinkster.io/tutorials/django-json-api/authentication
"""

import jwt

from django.conf import settings
from rest_framework import authentication, exceptions

from user.models import User
from flighty.messages.error import COULD_NOT_DECODE_TOKEN, DELETED_USER, DEACTIVATED_USER


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        """
        Called for every request

        Returns:
            None: Returns None when a token could not be decode

            token/user - Returns user's token for successful authentication
            """

        return self._validate_token(request)
    
    def _validate_token(self, request):

        """Validates jwt token
        
        Returns:
            JWT: validated token
        """

        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or len(auth_header) == 1 or len(auth_header) > 2:
            return None

        if auth_header[0].decode('utf-8').lower() != 'bearer':
            return None

        token = auth_header[1].decode('utf-8')
        
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the user and token. If not, throw an error.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = COULD_NOT_DECODE_TOKEN
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(DELETED_USER)

        if not user.is_active:
            raise exceptions.AuthenticationFailed(DEACTIVATED_USER)

        return (user, token)
