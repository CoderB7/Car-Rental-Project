from django.urls import path
from apps.cars.api.views import (
    CarListView,
    CarAddView,
    BrandListView
)

urlpatterns = [
    path('', CarListView.as_view(), name='car-list'),
    path('add/', CarAddView.as_view(), name='car-add'),

    path('brands/', BrandListView.as_view(), name='brand-list'),
]
