from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.exceptions import MethodNotAllowed

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from apps.shared.utils import success_response, error_response
from ..models import Car, Brand
from .serializers import (
    CarListSerializer,
    CarAddSerializer,
    CarDetailSerializer,
    CarDeleteSerializer,
    BrandListSerializer,
    BrandAddSerializer,
    BrandDetailSerializer,
    BrandCarListSerializer,
    BrandDeleteSerializer,
)


class CarAddView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CarAddSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully created Car object'
        )

class CarListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CarListSerializer

    def get_queryset(self):
        return Car.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of Cars'
        )


class CarDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CarDetailSerializer
    
    def get_object(self):
        car_uuid = self.kwargs.get("id")
        return get_object_or_404(Car, id=car_uuid)

    def retrieve(self, request, *args, **kwargs):
        car = self.get_object()
        serializer = self.get_serializer(car)
        return success_response(
            data=serializer.data,
            message='Car Details'
        )


class CarDeleteView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarDeleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        car_uuid = kwargs.get("id")
        serializer = self.get_serializer(data={"id": car_uuid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Car deleted successfully")


class BrandAddView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BrandAddSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully created Brand object'
        )


class BrandListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BrandListSerializer

    def get_queryset(self):
        return Brand.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of Brands'
        )


class BrandDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BrandDetailSerializer

    def get_object(self):
        brand_uuid = self.kwargs.get("id")
        return get_object_or_404(Brand, id=brand_uuid)
    
    def retrieve(self, request, *args, **kwargs):
        brand = self.get_object()
        serializer = self.get_serializer(brand)
        return success_response(
            data=serializer.data,
            message='Car Details'
        )

class BrandCarListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BrandCarListSerializer

    def get_queryset(self):
        brand_uuid = self.kwargs.get('id')
        return Car.objects.filter(brand=brand_uuid)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of Brand Cars'
        )


class BrandDeleteView(generics.CreateAPIView):
    queryset = Brand.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BrandDeleteSerializer

    def create(self, request, *args, **kwargs):
        brand_uuid = kwargs.get("id")
        serializer = self.get_serializer(data={"id": brand_uuid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Brand deleted successfully")


class SearchFilterView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transmission', 'fuel_type', 'type']
    search_fields = ['name', 'brand__name']
    ordering_fields = ['price', 'year', 'rating']

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.query_params.get('q')

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(brand__name__icontains=search_query)
            )
        
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['count'] = len(response.data['results'])
        return success_response(data=response.data)

