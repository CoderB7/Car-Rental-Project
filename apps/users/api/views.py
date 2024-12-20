from django.shortcuts import get_object_or_404

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.exceptions import MethodNotAllowed

from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    LoginSerializer,
    SendVerificationSerializer, 
    CheckVerificationSerializer, 
    RefreshTokenSerializer,
    PasswordResetSerializer,
    LogoutSerializer,
    DriverLicenceAddSerializer,
    DriverLicenceUpdateSerializer,
    DriverLicenceDeleteSerializer,
    DriverLicenceDetailSerializer,
)
from auth.custom_permissions import (
    IsSuperAdmin,
    IsCompanyAdmin,
    IsStaff,
    IsUser
)
from ..models import User, BlacklistedToken, DriverLicence
from apps.shared.utils import success_response, error_response

class SendVerification(generics.CreateAPIView):
    serializer_class = SendVerificationSerializer

    def create(self, request):
        context = {
            'action': request.data.get('action', None)
        }
        serializer = self.serializer_class(data=request.data, context=context) # context
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message='OTP sent to your email.')
        

class CheckVerification(generics.CreateAPIView):
    serializer_class = CheckVerificationSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message='OTP verified successfully, email verified.')


class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token, refresh_token = serializer.save()
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        return success_response(
            data=data,
            message='User registration successful.' 
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user

    def retrieve(self, request):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return success_response(
            data=serializer.data,
            message='User profile'
        )


class UserProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            data=serializer.data,
            message="User profile updated"
        )



class LogoutView(generics.CreateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = LogoutSerializer
    
    def create(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION', None).split(' ')[1]
        refresh_token = self.request.data.get('refresh_token', None)
        user = str(self.request.user.id)
        serializer = self.get_serializer(data={
            'user': user, 
            'access_token': access_token, 
            'refresh_token': refresh_token
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message='Logged out successfully')

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token, refresh_token = serializer.save()
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        return success_response(
            data=data,
            message='Login successful.'
        )
        
        
class RefreshTokenView(generics.CreateAPIView):
    serializer_class = RefreshTokenSerializer

    def create(self, request):
        refresh_token = self.request.data.get('refresh_token', None)
        if refresh_token is None:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'refresh_token': refresh_token})
        serializer.is_valid(raise_exception=True)
        new_access_token, new_refresh_token = serializer.save()
        data = {
            'access_token': new_access_token,
            'refresh_token': new_refresh_token,
        }
        return success_response(
            data=data,
            message='Token refreshed successfully.'
        )


class PasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]

    def get_object(self):
        email = self.request.data.get('email')
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return error_response(
                message='User with this email does not exist.',
                status=status.HTTP_404_NOT_FOUND,
            )
            
    def create(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return success_response(
            message="Password updated successfully."
        )


class DriverLicenceAddView(generics.CreateAPIView):
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    serializer_class = DriverLicenceAddSerializer

    def create(self, request):
        user_id = self.request.user.id
        serializer = self.get_serializer(data=request.data, user_id=user_id)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully added Driver Licence',
        )


class DriverLicenceDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DriverLicence.objects.all()
    permission_classes = [IsSuperAdmin | IsCompanyAdmin | IsStaff | IsUser]
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return DriverLicenceDetailSerializer
        elif self.request.method == "DELETE":
            return DriverLicenceDeleteSerializer
        return DriverLicenceUpdateSerializer

    def get_object(self):
        driver_licence_uuid = self.kwargs.get('id')
        return get_object_or_404(DriverLicence, id=driver_licence_uuid)

    def retrieve(self, request, *args, **kwargs):
        driver_licence = self.get_object()
        serializer = self.get_serializer(driver_licence)
        return success_response(
            data=serializer.data,
            message='Driver Licence details'
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Driver Licence object updated successfully", data=serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_destroy(instance)
        return success_response(message="Driver Licence deleted successfully")