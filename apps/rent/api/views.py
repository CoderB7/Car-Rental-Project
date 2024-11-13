from rest_framework import generics, status, permissions, filters

from django.shortcuts import get_object_or_404

from apps.shared.utils import success_response, error_response
from auth.custom_permissions import (
    IsSuperAdmin,
    IsCompanyAdmin,
    IsStaff,
    IsUser
)
from ..models import Booking
from .serializers import (
    CarBookingAddSerializer,
    CarBookingUpdateSerializer,
    CarBookingDetailListSerializer,
)


class CarBookingAddListView(generics.ListCreateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = CarBookingDetailListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarBookingAddSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        return Booking.objects.all()
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return success_response(
            data=serializer.data,
            message='Successfully booked selected car',
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of Car Bookings'
        )


class CarBookingDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CarBookingDetailListSerializer
        elif self.request.method == "DELETE":
            return CarBookingDetailListSerializer
        return CarBookingUpdateSerializer

    def get_object(self):
        booking_uuid = self.kwargs.get("id")
        return get_object_or_404(Booking, id=booking_uuid)
    
    def retrieve(self, request, *args, **kwargs):
        booking = self.get_object()
        serializer = self.get_serializer(booking)
        return success_response(
            data=serializer.data,
            message='Car Booking Detail'
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Car Booking object updated successfully", data=serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(message="Booking deleted successfully")

