from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from apps.users.models import User, Review
from ..models import ( 
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


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandCarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'name', 'transmission', 'price', 'image'] 

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.brand:
            response["brand_name"] = instance.brand.name
        return response


class BrandUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

    def validate_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError('Provided year must be less than the current year.')
        return value
    

class BrandDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = []


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


class CarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'name', 'type', 'transmission', 'fuel_type', 'price', 'image'] 

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.brand:
            response["brand_name"] = instance.brand.name
        return response
    

class CarDetailSerializer(serializers.ModelSerializer):
    brand = BrandDetailSerializer()

    class Meta:
        model = Car
        fields = '__all__'
    

class CarUpdateSerializer(serializers.ModelSerializer):
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


class CarDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = []


class ReviewAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']                                                                                                                                                                                                                                                                                                                                                                   

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        self.car_id = kwargs.pop('car_id', None)
        super(ReviewAddSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.car:
            response["car_name"] = instance.car.name
        if instance.user:
            response["user_name"] = f'{instance.user.first_name} {instance.user.last_name}'
        return response

    def validate_rating(self, value):
        if not value:
            raise serializers.ValidationError("Rating is required")
        print(type(value))
        if value > 5 and value < 0:
            raise serializers.ValidationError("Rating should be less than 5 and more than 0")
        return value

    # def validate_car(self, value):
    #     if not value:
    #         raise serializers.ValidationError("Car instance is required")
    #     if not Review.objects.filter(car=value).exists():
    #         raise serializers.ValidationError("Car does not exist")
    #     return value

    def create(self, validated_data):
        user = User.objects.get(id=self.user_id)
        car = Car.objects.get(id=self.car_id)
        validated_data['user'] = user
        validated_data['car'] = car
        return Review.objects.create(**validated_data)


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.car:
            response["car_name"] = instance.car.name
        if instance.user:
            response["user_name"] = f'{instance.user.first_name} {instance.user.last_name}'
        return response
    

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.car:
            response["car_name"] = instance.car.name
        if instance.user:
            response["user_name"] = f'{instance.user.first_name} {instance.user.last_name}'
        return response


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, value):
        if not value:
            raise serializers.ValidationError("Rating is required")
        if value > 5 and value < 0:
            raise serializers.ValidationError("Rating should be less than 5 and more than 0")
        return value


class ReviewDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = []

    