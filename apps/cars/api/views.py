from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.exceptions import MethodNotAllowed

from apps.shared.utils import success_response, error_response
from ..models import Car, Brand
from .serializers import (
    CarListSerializer,
    BrandListSerializer,
    CarAddSerializer,
)


class CarAddView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CarAddSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        print('done')
        return success_response(
            data=serializer.data,
            message='Successfully created Car object'
        )

class CarListView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CarListSerializer

    def get_queryset(self):
        return Car.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        cars = self.get_queryset()
        serializer = self.get_serializer(cars)
        return success_response(
            data=serializer.data,
            message='List of Cars'
        )


class BrandListView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BrandListSerializer

    def get_object(self):
        return Brand.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        brands = self.get_object()
        serializer = self.get_serializer(brands)
        return success_response(
            data=serializer.data,
            message='List of Brands'
        )


