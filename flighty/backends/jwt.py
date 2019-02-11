"""JWT Authentication module

Raises:
    exceptions.AuthenticationFailed: Raise this exception when authentication failed
"""

import jwt

from django.conf import settings
from rest_framework import authentication, exceptions

from user.models import User
from flighty.messages.error import COULD_NOT_DECODE_TOKEN, DELETED_USER, DEACTIVATED_USER


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires authentication. 
        `authenticate` has two possible return values:
        1) `None` - We return `None` if we do not wish to authenticate. Usually
                    this means we know authentication will fail. An example of
                    this is when the request does not include a token in the
                    headers.
        2) `(user, token)` - We return a user/token combination when 
                             authentication is successful.
                            If neither case is met, that means there's an error 
                            and we do not return anything.
                            We simple raise the `AuthenticationFailed` 
                            exception and let Django REST Framework
                            handle the rest.
        """
        
        request.user = None

        return self._validate_token(request)
    
    def _validate_token(self, request):

        """Validates jwt token
        
        Returns:
            JWT: validated token
        """

        auth_header = authentication.get_authorization_header(request).split()
        prefix = 'bearer'

        if not auth_header:
            return None
        
        if len(auth_header) == 1:
            # Invalid token header. No credentials provided. Do not attempt to
            # authenticate.
            return None

        elif len(auth_header) > 2:
            # Invalid token header. The Token string should not contain spaces. Do
            # not attempt to authenticate.
            return None

        auth_header_prefix = auth_header[0].decode('utf-8')
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
