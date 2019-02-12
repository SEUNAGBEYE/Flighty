from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import (RegistrationSerializer, LoginSerializer, UserSerializer)

from rest_framework.generics import RetrieveAPIView


from .models import UserProfile
from .messages.success import USER_CREATED, LOGIN_SUCCESSFULL, PROFILE_UPDATED, USER_RETRIEVED

from flighty.response import success_response


class RegistrationAPIView(APIView):
    """Handles users registration"""

    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """Creates a user

            Args:
                request (request object): Django request object
            Returns:
                JSON: Newly crearted user
        """
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(serializer.data, USER_CREATED, status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        """Handles user login"""
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return success_response(serializer.data, LOGIN_SUCCESSFULL,status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """Gets user data"""
        serializer = self.serializer_class(request.user)

        return success_response(serializer.data, USER_RETRIEVED,status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data

        profile_data = {
            'userprofile': data
        }

        serializer = self.serializer_class(
            request.user, data=profile_data, partial=True, context={'deleteImage': request.query_params.get('deleteImage'), 'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(serializer.data, PROFILE_UPDATED, status.HTTP_200_OK)
