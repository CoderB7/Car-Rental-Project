from django.urls import path
from apps.rent.api.views import (
    CarBookingAddListView,
    CarBookingDetailUpdate,
    CarBookingDeleteView
)

urlpatterns = [
    path('booking/add/', CarBookingAddListView.as_view(), name='car-booking-add'),
    path('booking/list/', CarBookingAddListView.as_view(), name='car-booking-list'),
    path('booking/<uuid:id>/update/', CarBookingDetailUpdate.as_view(), name='car-booking-update'),
    path('booking/<uuid:id>/detail/', CarBookingDetailUpdate.as_view(), name='car-booking-detail'),
    path('booking/<uuid:id>/delete/', CarBookingDeleteView.as_view(), name='car-booking-delete')
]

