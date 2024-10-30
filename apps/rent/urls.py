from django.urls import path
from apps.rent.api.views import (
    CarBookCartView,
)

urlpatterns = [
    path('add/cart/', CarBookCartView.as_view(), name='car-add-cart'),
]

