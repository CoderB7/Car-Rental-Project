from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.permissions import AllowAny


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
from ..models import Car, Brand
from apps.users.models import Review
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


class CarAddListView(generics.ListCreateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin]
    serializer_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarAddSerializer
        return CarListSerializer

    def get_queryset(self):
        return Car.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully created Car object'
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of Cars'
        )


class CarDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin]
    queryset = Car.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CarDetailSerializer
        elif self.request.method == "DELETE":
            return CarDeleteSerializer
        return CarUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

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
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True) # partial true means put and patch does the same job
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Car object updated successfully", data=serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_destroy(instance)
        return success_response(message="Car deleted successfully")


class BrandAddListView(generics.ListCreateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin]
    serializer_class = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BrandAddSerializer
        return BrandListSerializer
    
    def get_queryset(self):
        return Brand.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully created Brand object'
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of Brands'
        )
    

class BrandDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    permission_classes = [IsSuperAdmin | IsCompanyAdmin]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BrandDetailSerializer
        elif self.request.method == "DELETE":
            return BrandDeleteSerializer
        return BrandUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

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
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message='Brand object updated successfully', data=serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_destroy(instance)
        return success_response(message="Car deleted successfully")


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


class ReviewAddListView(generics.ListCreateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewAddSerializer
        return ReviewListSerializer

    def get_queryset(self):
        car_uuid = self.kwargs.get('car_id', None)
        return Review.objects.filter(car=car_uuid)

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
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of car reviews'
        )

# ### review list ni qaytadan korish kere
# class CarReviewListView(generics.ListAPIView):
#     permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
#     serializer_class = ReviewListSerializer

#     def get_queryset(self):
#         car_uuid = self.kwargs.get('car_id', None)
#         return Review.objects.filter(car=car_uuid)
    
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         print(queryset)
#         serializer = self.get_serializer(queryset, many=True)
#         return success_response(
#             data=serializer.data,
#             message='List of car reviews'
#         )


class UserReviewListView(generics.ListAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Review.objects.filter(user=user_id)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of user reviews'
        )


class ReviewDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReviewDetailSerializer
        elif self.request.method == "DELETE":
            return ReviewDeleteSerializer
        return ReviewUpdateSerializer

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
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message='Review object updated successfully', data=serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_destroy(instance)
        return success_response(message='Review deleted successfully')

# class ReviewUpdateView(generics.UpdateAPIView):
#     queryset = Review.objects.all()
#     permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff]
#     serializer_class = ReviewUpdateSerializer
    
#     def get_object(self):
#         review_uuid = self.kwargs.get('review_id')
#         return get_object_or_404(Review, id=review_uuid)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return success_response(message='Review object updated successfully', data=serializer.data)


# class ReviewDeleteView(generics.DestroyAPIView):
#     queryset = Review.objects.all()
#     permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff]
#     serializer_class = ReviewDeleteSerializer

#     def get_object(self):
#         review_uuid = self.kwargs.get('review_id')
#         return get_object_or_404(Review, id=review_uuid)

#     def delete(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_destroy(instance)
#         return success_response(message='Review deleted successfully')
    