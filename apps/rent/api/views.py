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
    CarBookingListSerializer,
    CarBookingDeleteSerializer,
    CarBookingUpdateSerializer,
    CarBookingDetailSerializer,

)


class CarBookingAddListView(generics.ListCreateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarBookingAddSerializer
        return CarBookingListSerializer
    
    def get_queryset(self):
        return Booking.objects.all()

    def create(self, request):
        user_id = self.request.user.id
        serializer = self.get_serializer(data=request.data, user_id=user_id)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully booked selected car',
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print('entered')
        return success_response(
            data=serializer.data,
            message='List of Car Bookings'
        )


class CarBookingDetailUpdate(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CarBookingDetailSerializer
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


class CarBookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = CarBookingDeleteSerializer
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]

    def delete(self, request, *args, **kwargs):
        booking_uuid = kwargs.get("id")
        serializer = self.get_serializer(data={"id": booking_uuid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Booking deleted successfully")



