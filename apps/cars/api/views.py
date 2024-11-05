from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.exceptions import MethodNotAllowed

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from auth.custom_permissions import (
    IsSuperAdmin,
    IsCompanyAdmin,
    IsStaff,
    IsUser
)
from apps.shared.utils import success_response, error_response
from ..models import Car, Brand, Review
from ..filters import CarFilter
from .serializers import (
    CarListSerializer,
    CarAddSerializer,
    CarDetailSerializer,
    CarUpdateSerializer,
    CarDeleteSerializer,
    BrandListSerializer,
    BrandAddSerializer,
    BrandDetailSerializer,
    BrandUpdateSerializer,
    BrandCarListSerializer,
    BrandDeleteSerializer,
    ReviewAddSerializer,
    ReviewListSerializer,
    ReviewDetailSerializer,
    ReviewUpdateSerializer,
    ReviewDeleteSerializer
)


class CarAddView(generics.CreateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin]
    serializer_class = CarAddSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully created Car object'
        )

class CarListView(generics.ListAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = CarListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

    def get_queryset(self):
        return Car.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of Cars'
        )


class CarDetailView(generics.RetrieveAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = CarDetailSerializer
    
    def get_object(self):
        car_uuid = self.kwargs.get("id")
        return get_object_or_404(Car, id=car_uuid)

    def retrieve(self, request, *args, **kwargs):
        car = self.get_object()
        serializer = self.get_serializer(car)
        return success_response(
            data=serializer.data,
            message='Car Details'
        )


class CarUpdateView(generics.UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarUpdateSerializer
    permission_classes = [IsSuperAdmin | IsCompanyAdmin]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True) # partial true means put and patch does the same job
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Car object updated successfully", data=serializer.data)


class CarDeleteView(generics.DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarDeleteSerializer
    permission_classes = [IsSuperAdmin | IsCompanyAdmin]

    def delete(self, request, *args, **kwargs):
        car_uuid = kwargs.get("id")
        serializer = self.get_serializer(data={"id": car_uuid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Car deleted successfully")


class BrandAddView(generics.CreateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin]
    serializer_class = BrandAddSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully created Brand object'
        )


class BrandListView(generics.ListAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = BrandListSerializer

    def get_queryset(self):
        return Brand.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of Brands'
        )


class BrandDetailView(generics.RetrieveAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = BrandDetailSerializer

    def get_object(self):
        brand_uuid = self.kwargs.get("id")
        return get_object_or_404(Brand, id=brand_uuid)
    
    def retrieve(self, request, *args, **kwargs):
        brand = self.get_object()
        serializer = self.get_serializer(brand)
        return success_response(
            data=serializer.data,
            message='Car Details'
        )


class BrandUpdateView(generics.UpdateAPIView):
    queryset = Brand.objects.all()
    permission_classes = [IsSuperAdmin | IsCompanyAdmin]
    serializer_class = BrandUpdateSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message='Brand object updated successfully', data=serializer.data)
    

class BrandCarListView(generics.ListAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = BrandCarListSerializer

    def get_queryset(self):
        brand_uuid = self.kwargs.get('id')
        return Car.objects.filter(brand=brand_uuid)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of Brand Cars'
        )


class BrandDeleteView(generics.DestroyAPIView):
    queryset = Brand.objects.all()
    permission_classes = [IsSuperAdmin | IsCompanyAdmin]
    serializer_class = BrandDeleteSerializer

    def delete(self, request, *args, **kwargs):
        brand_uuid = kwargs.get("id")
        serializer = self.get_serializer(data={"id": brand_uuid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Brand deleted successfully")


class SearchView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'brand__name']
    ordering_fields = ['price', 'year', 'rating']

    def get_queryset(self): # custom queryset
        queryset = super().get_queryset()

        search_query = self.request.query_params.get('q')

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(brand__name__icontains=search_query)
            )
        
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['count'] = len(response.data['results'])
        return success_response(data=response.data)


class ReviewAddView(generics.CreateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = ReviewAddSerializer

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id
        car_id = self.kwargs.get('car_id', None)
        serializer = self.get_serializer(data=request.data, user_id=user_id, car_id=car_id)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully created Review',
        )

### review list ni qaytadan korish kere
class CarReviewListView(generics.ListAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        car_uuid = self.kwargs.get('car_id', None)
        return Review.objects.filter(car=car_uuid)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of car reviews'
        )


class UserReviewListView(generics.ListAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = ReviewListSerializer

    def get_queryset(self, user_id):
        return Review.objects.filter(user=user_id)
    
    def list(self, request, *args, **kwargs):
        user_id = self.request.user.id
        queryset = self.get_queryset(user_id)
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of user reviews'
        )


class ReviewDetailView(generics.RetrieveAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = ReviewDetailSerializer

    def get_object(self):
        review_uuid = self.kwargs.get("review_id")
        return get_object_or_404(Review, id=review_uuid)

    def retrieve(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = self.get_serializer(review)
        return success_response(
            data=serializer.data,
            message='Review detail'
        ) 


class ReviewUpdateView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff]
    serializer_class = ReviewUpdateSerializer
    
    def get_object(self):
        review_uuid = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_uuid)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message='Review object updated successfully', data=serializer.data)


class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff]
    serializer_class = ReviewDeleteSerializer

    def get_object(self):
        review_uuid = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_uuid)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(message='Review deleted successfully')
    