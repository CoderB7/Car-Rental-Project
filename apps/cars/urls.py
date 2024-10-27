from django.urls import path
from apps.cars.api.views import (
    CarListView,
    CarAddView,
    CarDetailView,
    CarDeleteView,
    BrandListView,
    BrandAddView,
    BrandDetailView,
    BrandCarListView,
    BrandDeleteView,
    SearchFilterView,
)

urlpatterns = [
    path('', CarListView.as_view(), name='car-list'),
    path('add/', CarAddView.as_view(), name='car-add'),
    path('<uuid:id>/', CarDetailView.as_view(), name='car-detail'),
    path('<uuid:id>/delete/', CarDeleteView.as_view(), name='car-delete'),

    path('brands/add/', BrandAddView.as_view(), name='brand-add'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('brands/<uuid:id>/', BrandDetailView.as_view(), name='brand-detail'),
    path('brand/<uuid:id>/', BrandCarListView.as_view(), name='brand-car-list'),
    path('brand/<uuid:id>/delete/', BrandDeleteView.as_view(), name='brand-delete'),

    path('search/', SearchFilterView.as_view(), name='car-search')
]
