from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.exceptions import MethodNotAllowed

from apps.shared.utils import success_response, error_response
from ..models import Car, Brand
from .serializers import (
    CarListSerializer,
    BrandListSerializer,
    BrandAddSerializer,
    CarAddSerializer,
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


