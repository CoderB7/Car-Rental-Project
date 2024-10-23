import jwt
import datetime

from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.exceptions import MethodNotAllowed

from .serializers import UserSerializer, UserProfileSerializer, LoginSerializer
from .serializers import (
    SendVerificationSerializer, 
    CheckVerificationSerializer, 
    RefreshTokenSerializer,
    PasswordResetSerializer,
)

from apps.shared.redis_client import blacklist_token
from ..models import User, BlacklistedToken
from drf_yasg.utils import swagger_auto_schema

class SendVerification(generics.CreateAPIView):
    serializer_class = SendVerificationSerializer

    def create(self, request):
        context = {
            'action': request.data.get('action', None)
        }
        serializer = self.serializer_class(data=request.data, context=context) # context
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_200_OK)


class CheckVerification(generics.CreateAPIView):
    serializer_class = CheckVerificationSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'OTP verified successfully, email verified.'}, status=status.HTTP_200_OK)


class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token, refresh_token = serializer.save()
        
        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=True, samesite='Strict')
        response.data = {
            'access_token': access_token,
        }
        return response


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user

    def retrieve(self, request):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        refresh_token = request.COOKIES.get('refresh_token', None)
        access_token = request.META.get('HTTP_AUTHORIZATION', None).split(' ')[1]
        if refresh_token and access_token:
            try:
                BlacklistedToken.blacklist_token(access_token, refresh_token)
                response = Response()
                response.delete_cookie('refresh_token')
                response.data = {
                    'message': 'Logged out successfully',
                }
                response.status_code = status.HTTP_200_OK
                return response
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Refresh token not found.'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token, refresh_token = serializer.save()
        
        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=True, samesite='Strict')
        response.data = {
            'access_token': access_token,
        }
        return response
        
        
class RefreshTokenView(generics.CreateAPIView):
    serializer_class = RefreshTokenSerializer

    def create(self, request):
        refresh_token = request.COOKIES.get('refresh_token', None)

        if refresh_token is None:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'refresh_token': refresh_token})
        serializer.is_valid(raise_exception=True)
        new_access_token, new_refresh_token = serializer.save()

        response = Response()
        response.set_cookie(key='refresh_token', value=new_refresh_token, httponly=True, secure=True, samesite='Strict')
        response.data = {
            'access_token': new_access_token,
        }
        response.status_code = status.HTTP_200_OK
        return response


class PasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        email = self.request.data.get('email')
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

