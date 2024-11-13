import pytz # type: ignore
from datetime import datetime

from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from apps.users.models import User
from ..models import (
    Booking, 
    RentHistory
)

class ISO8601DateTimeField(serializers.DateTimeField):
    def to_internal_value(self, value):
        try:
            # Parse the datetime string using the expected ISO 8601 format
            return datetime.strptime(value, '%Y-%m-%d').replace(tzinfo=pytz.utc)
        except ValueError:
            self.fail('invalid')


class CarBookingAddSerializer(serializers.ModelSerializer):
    rental_start = ISO8601DateTimeField()
    rental_end = ISO8601DateTimeField()

    class Meta:
        model = Booking
        fields = ['car', 'pickup_location', 'dropoff_location', 'total_cost', 'rental_start', 'rental_end', 'status', 'agreement_signed']

    def validate_rental_start(self, value):
        if not value:
            raise serializers.ValidationError('Rental start date is required')
        current_date = timezone.now()
        if value < current_date:
            raise serializers.ValidationError('Provided date must be later than the current data')
        return value

    def validate_rental_end(self, value):
        if not value:
            raise serializers.ValidationError('Rental end date is required')
        current_date = timezone.now()
        if value < current_date:
            raise serializers.ValidationError('Provided date must be later than the current date')
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user
        rental_start = attrs.get('rental_start', None)
        rental_end = attrs.get('rental_end', None)
        car_id = attrs.get('car', None)
        
        if Booking.objects.filter(user=user.id, car=car_id).exists():
            raise serializers.ValidationError("Already booked")
        if rental_end < rental_start:
            raise serializers.ValidationError('Rental end time must be later than the rental start time')
        return attrs


class CarBookingDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.car:
            response["car_name"] = instance.car.name
        if instance.user:
            response["user_name"] = f'{instance.user.first_name} {instance.user.last_name}'
        return response



class CarBookingUpdateSerializer(serializers.ModelSerializer):
    rental_start = ISO8601DateTimeField()
    rental_end = ISO8601DateTimeField()

    class Meta:
        model = Booking
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.car:
            response["car_name"] = instance.car.name
        if instance.user:
            response["user_name"] = f'{instance.user.first_name} {instance.user.last_name}'
        return response

    def validate_rental_start(self, value):
        if not value:
            raise serializers.ValidationError('Rental start date is required')
        current_date = timezone.now()
        if value < current_date:
            raise serializers.ValidationError('Provided date must be later than the current data')
        return value

    def validate_rental_end(self, value):
        if not value:
            raise serializers.ValidationError('Rental end date is required')
        current_date = timezone.now()
        if value < current_date:
            raise serializers.ValidationError('Provided date must be later than the current date')
        return value

    def validate(self, attrs):
        rental_start = attrs.get('rental_start', None)
        rental_end = attrs.get('rental_end', None)
        if rental_end < rental_start:
            raise serializers.ValidationError('Rental end time must be later than the rental start time')
        return attrs

    