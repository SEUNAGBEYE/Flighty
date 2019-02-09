from rest_framework import serializers
from .models import Flight
from flighty.validators.choice_validators import choice_validator


class FlightSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of Flight objects."""

    id = serializers.IntegerField(read_only=True)
    departure_date = serializers.DateTimeField()
    return_date = serializers.DateTimeField(default='')
    origin = serializers.CharField(max_length = 100)
    destination = serializers.CharField(max_length = 100)
    airline_code = serializers.CharField(max_length = 100)
    status = serializers.CharField(max_length = 100, validators=[choice_validator(Flight.STATUS_CHOICES)], source='get_status_display')
    flight_class = serializers.CharField(max_length = 100, validators=[choice_validator(Flight.CLASS_CHOICES)], required=False, source='get_flight_class_display')
    fare = serializers.FloatField()
    one_way = serializers.BooleanField()
    stops = serializers.IntegerField(default=0)

    def validate(self, data):
        """Validates flights data
        
            Args:
                data (dict): flight's data
            
            Raises:
                serializers.ValidationError: serializer's error
        
        Returns:
            flight data
        """

        one_way = data.get('one_way', ' ')
        return_date = data.get('return_date', ' ')
        if not one_way and not return_date:
            raise serializers.ValidationError('return_date must be provided for returned flights')
        
        if (one_way and return_date) or one_way and not return_date:
            data.pop('return_date', '')

        return data

    class Meta:
        model = Flight
        fields = (
            'id',
            'departure_date',
            'return_date',
            'origin',
            'destination',
            'airline_code',
            'status',
            'fare',
            'one_way',
            'stops',
            'flight_class'
        )
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        """Updates Flights"""


        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance
    
    def create(self):
        """Creates Flights"""
        
        return Flight.objects.get_or_create(**self.validated_data)