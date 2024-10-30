import pytz
from datetime import datetime

from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from ..models import (
    Cart, 
    RentHistory
)

class ISO8601DateTimeField(serializers.DateTimeField):
    def to_internal_value(self, value):
        try:
            # Parse the datetime string using the expected ISO 8601 format
            return datetime.strptime(value, '%Y-%m-%d').replace(tzinfo=pytz.utc)
        except ValueError:
            self.fail('invalid')


class CarBookCartSerializer(serializers.ModelSerializer):
    rental_start = ISO8601DateTimeField()
    rental_end = ISO8601DateTimeField()

    class Meta:
        model = Cart
        fields = '__all__'

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

    def create(self, validated_data):
        return Cart.objects.create(**validated_data)
