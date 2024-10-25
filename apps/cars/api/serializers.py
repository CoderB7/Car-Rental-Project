from datetime import datetime

from rest_framework import serializers

from ..models import ( 
    TransmissionChoices, 
    Brand, 
    Car
)

class BrandAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
    
    def validate_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError('Provided year must be less than the current year.')
        return value


class BrandListSerializer(serializers.Serializer):
    name = serializers.CharField()
    logo = serializers.ImageField()


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandCarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'name', 'transmission', 'price', 'image'] 


class CarAddSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())

    class Meta:
        model = Car
        fields = '__all__'

    def validate_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError('Provided year must be less than the current year.')
        return value

    def validate_mileage(self, value):
        if value < 0:
            raise serializers.ValidationError('Mileage cannot be negative.')
        return value

    def validate_doors(self, value):
        if value < 2 or value > 5:
            raise serializers.ValidationError('Doors must be between 2 and 5.')
        return value

    def validate_seats(self, value):
        if value < 1 or value > 9:
            raise serializers.ValidationError('Seats must be between 1 and 9.')
        return value

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError('Rating must be between 0 and 5.')
        return value


class CarListSerializer(serializers.Serializer):
    name = serializers.CharField()
    brand = serializers.CharField()
    transmission = serializers.ChoiceField(choices=TransmissionChoices.choices())
    price = serializers.FloatField()
    image = serializers.ImageField()


class CarDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


