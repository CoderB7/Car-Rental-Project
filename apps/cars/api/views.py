from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.exceptions import MethodNotAllowed

from django.shortcuts import get_object_or_404

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

