from django.urls import path
from apps.cars.api.views import (
    CarListView,
    CarAddView,
    BrandListView,
    BrandAddView,
)

urlpatterns = [
    path('', CarListView.as_view(), name='car-list'),
    path('add/', CarAddView.as_view(), name='car-add'),

    path('brands/add/', BrandAddView.as_view(), name='brand-add'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
]
