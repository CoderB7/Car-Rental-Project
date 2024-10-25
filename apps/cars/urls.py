from django.urls import path
from apps.cars.api.views import (
    CarListView,
    CarAddView,
    CarDetailView,
    BrandListView,
    BrandAddView,
    BrandDetailView,
    BrandCarListView,
)

urlpatterns = [
    path('', CarListView.as_view(), name='car-list'),
    path('add/', CarAddView.as_view(), name='car-add'),
    path('<uuid:id>/', CarDetailView.as_view(), name='car-detail'),

    path('brands/add/', BrandAddView.as_view(), name='brand-add'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('brands/<uuid:id>/', BrandDetailView.as_view(), name='brand-detail'),
    path('brand/<uuid:id>/', BrandCarListView.as_view(), name='brand-car-list'),

]
