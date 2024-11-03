import django_filters
from django_filters import rest_framework as filters
from .models import Car


class CarFilter(filters.FilterSet):
    transmission = filters.CharFilter(field_name='transmission')
    fuel_type = filters.CharFilter(field_name='fuel_type')
    type = filters.CharFilter(field_name='type')
    
    price = filters.NumberFilter()
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    
    year = filters.NumberFilter(field_name='year', lookup_expr='year')
    year__gt = filters.NumberFilter(field_name='year', lookup_expr='year__gt')
    year__lt = filters.NumberFilter(field_name='year', lookup_expr='year__lt')
    
    brand__name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Car
        fields = [
            'transmission', 
            'fuel_type',
            'type',
            'price',
            'year',
            'brand'
        ]
    

