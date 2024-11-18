from django.urls import path
from apps.cars.api.views import (
    CarAddListView,
    CarDetailUpdateDeleteView,
    BrandAddListView,
    BrandDetailUpdateDeleteView,
    BrandCarListView,
    SearchView,
    ReviewAddListView,
    ReviewDetailUpdateDeleteView,
)

urlpatterns = [
    # path('', CarAddListView.as_view(), name='car-add-list'),
    path('<uuid:id>/', CarDetailUpdateDeleteView.as_view(), name='car-detail-update-delete'),
    
    path('brand/', BrandAddListView.as_view(), name='brand-add'),
    path('brand/<uuid:id>/', BrandDetailUpdateDeleteView.as_view(), name='brand-detail-update-delete'),
    path('brand/<uuid:id>/cars/', BrandCarListView.as_view(), name='brand-car-list'),

    path('search/', SearchView.as_view(), name='car-search'),

    path('<uuid:car_id>/review/', ReviewAddListView.as_view(), name='review-add-list'),
    path('reviews/<uuid:review_id>/', ReviewDetailUpdateDeleteView.as_view(), name='car-review-detail-update-delete'),
]
