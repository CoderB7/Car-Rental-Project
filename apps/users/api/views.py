import jwt
import datetime

from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .serializers import UserSerializer, UserProfileSerializer, LoginSerializer, OTPVerificationSerializer
from ..models import User
from .utils import generate_otp, is_otp_unique, send_otp_via_email, decrypt_access_token, decrypt_refresh_token, generate_jwt_token

OTP_LIFETIME=120

# Create your views here.
class RegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email", None)
            password = serializer.validated_data['password']
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)
            otp = generate_otp()
            while not is_otp_unique(email, otp):
                otp = generate_otp()
            cache.set(f"{email}_otp", otp, timeout=OTP_LIFETIME)  # Store OTP in cache for 5 minutes
            send_otp_via_email(email, otp)  # Send OTP via email
            return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('refresh_token')
        response.data = {
            'message': 'success',
        }
        return response

class LoginView(APIView): # Create API View
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data['email']
            password = request.data['password']

            user = authenticate(username=email, password=password)

            if user is not None:
                payload = {
                    'user_id': user.id,
                    'iat': datetime.datetime.now(datetime.timezone.utc) # issued at
                }
                # Convert datetime to Unix timestamps
                payload['iat'] = int(payload['iat'].timestamp())
                access_token, refresh_token = generate_jwt_token(payload)

                #RESPONSE#
                response = Response()
                response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=True, samesite='Strict')
                response.data = {
                    'access_token': access_token,
                }
                response.status_code = status.HTTP_200_OK
                return response
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = decrypt_refresh_token(refresh_token)
            user_id = payload['payload']['user_id']
            new_payload = {
                'user_id': user_id,
                'iat': datetime.datetime.now(datetime.timezone.utc)
            }
            # Convert datetime to Unix timestamps
            new_payload['iat'] = int(payload['iat'].timestamp())
            new_access_token, new_refresh_token = generate_jwt_token(new_payload)
            
            response = Response()
            response.set_cookie(key='refresh_token', value=new_refresh_token, httponly=True, secure=True, samesite='Strict')
            response.data = {
                'access_token': new_access_token,
            }
            response.status_code = status.HTTP_200_OK
            return response
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            cached_otp = cache.get(f'{email}_otp')
            if cached_otp and otp == cached_otp:
                # OTP matched, user is authenticated
                password = request.data.get('password')
                if not password:
                    return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)
                user = User.objects.create_user(email=email, password=password)  
                payload = {
                    'user_id': user.id,
                    'iat': datetime.datetime.now(datetime.timezone.utc)
                }
                # Convert datetime to Unix timestamps
                payload['iat'] = int(payload['iat'].timestamp())
                access_token, refresh_token = generate_jwt_token(payload)
                cache.delete(f"{email}_otp") # Remove OTP from cache

                response = Response()
                response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=True, samesite='Strict')
                response.data = {
                    'access_token': access_token,
                }
                return response
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



