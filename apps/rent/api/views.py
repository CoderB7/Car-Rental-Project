from rest_framework import generics, status, permissions, filters

from django.shortcuts import get_object_or_404

from apps.shared.utils import success_response, error_response
from ..models import Booking
from .serializers import (
    CarBookCartSerializer,
)


class CarBookCartView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CarBookCartSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully staged selected car',
        )


