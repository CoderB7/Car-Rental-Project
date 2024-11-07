from django.urls import path
from apps.rent.api.views import (
    CarBookingAddListView,
    CarBookingDetailUpdateDeleteView
)

urlpatterns = [
    path('booking/', CarBookingAddListView.as_view(), name='car-booking-add'),
    path('booking/<uuid:id>/', CarBookingDetailUpdateDeleteView.as_view(), name='car-booking-update'),
]

