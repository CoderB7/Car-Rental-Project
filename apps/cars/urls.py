from django.urls import path
from apps.cars.api.views import (
    CarListView,
    CarAddView,
    CarDetailView,
    CarUpdateView,
    CarDeleteView,
    BrandListView,
    BrandAddView,
    BrandDetailView,
    BrandCarListView,
    BrandUpdateView,
    BrandDeleteView,
    SearchView,
    ReviewAddView,
    CarReviewListView,
    ReviewDetailView,
    ReviewUpdateView,
    ReviewDeleteView,
)

urlpatterns = [
    path('', CarListView.as_view(), name='car-list'),
    path('add/', CarAddView.as_view(), name='car-add'),
    path('<uuid:id>/', CarDetailView.as_view(), name='car-detail'),
    path('<uuid:id>/update/', CarUpdateView.as_view(), name='car-update'),
    path('<uuid:id>/delete/', CarDeleteView.as_view(), name='car-delete'),

    path('brands/add/', BrandAddView.as_view(), name='brand-add'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('brands/<uuid:id>/', BrandDetailView.as_view(), name='brand-detail'),
    path('brand/<uuid:id>/', BrandCarListView.as_view(), name='brand-car-list'),
    path('brand/<uuid:id>/update/', BrandUpdateView.as_view(), name='brand-update'),
    path('brand/<uuid:id>/delete/', BrandDeleteView.as_view(), name='brand-delete'),

    path('search/', SearchView.as_view(), name='car-search'),

    path('<uuid:car_id>/review/add/', ReviewAddView.as_view(), name='review-create'),
    path('<uuid:car_id>/review/list/', CarReviewListView.as_view(), name='car-review-list'),
    path('<uuid:review_id>/review/detail/', ReviewDetailView.as_view(), name='car-review-detail'),
    path('<uuid:review_id>/review/update/', ReviewUpdateView.as_view(), name='car-review-update'),
    path('<uuid:review_id>/review/delete/', ReviewDeleteView.as_view(), name='car-review-delete'),
]
