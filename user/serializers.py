"""User Serializers

Reference : https://thinkster.io/tutorials/django-json-api/authentication
"""

from datetime import datetime
import os

from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, UserProfile
from .messages.error import LOGIN_FAIL



class RegistrationSerializer(serializers.ModelSerializer):
    """Serializes registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # sets this field to read only
    token = serializers.CharField(max_length=255, read_only=True)

    #pylint: disable=missing-docstring
    class Meta:

        model = User
        fields = ['email', 'password', 'token']

    def create(self, validated_data):
        """Creates a user"""
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """Validates login data"""

        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # passed email as username because we set USERNAME_FIELD to email
        user = authenticate(username=email, password=password)

        # Raise an exception if no user was found
        if user is None:
            raise serializers.ValidationError(
                LOGIN_FAIL
            )

        # Raise an exception if user has been deactivated
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'firstname': user.userprofile.first_name,
            'token': user.token
        }

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes users profiles"""
    city = serializers.CharField(allow_blank=True, required=False)
    house_address = serializers.CharField(allow_blank=True, required=False)
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    state = serializers.CharField(allow_blank=True, required=False)
    image = serializers.ImageField()

    #pylint: disable=missing-docstring
    class Meta:
        model = UserProfile
        fields = ('image', 'city', 'house_address', 'last_name','first_name', 'state')

class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    userprofile = UserProfileSerializer()

    #pylint: disable=missing-docstring
    class Meta:
        model = User
        fields = ('email', 'password', 'token', 'userprofile')

        read_only_fields = ('token',)

    def validate(self, data):
        """
        Validates user profile info
        """
        delete_image = self.context.get('deleteImage')
        user = self.context.get('user')
        image_path = user.userprofile.image
        if delete_image:
            data['userprofile']['image'] = ''
            if image_path:
                try:
                    os.remove(image_path.path)
                except FileNotFoundError:
                    print('File not found')

        image = data['userprofile'].get('image')
        if not delete_image and image:
            username = user.email.split('@')[0]
            ext = image.name.split('.')[-1]
            data['userprofile']['image'].name = f'{image}-{username}-{datetime.now()}.{ext}'
        return data

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Removes the password and userprofile from the serialized data
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('userprofile', {})


        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` handles all password related securities
            instance.set_password(password)

        instance.save()

        for (key, value) in profile_data.items():
            setattr(instance.userprofile, key, value)
     
        instance.userprofile.save()

        return instance