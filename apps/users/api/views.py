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
from .serializers import SendVerificationSerializer, CheckVerificationSerializer
from ..models import User
from .utils import generate_otp, is_otp_unique, send_otp_via_email, decrypt_access_token, decrypt_refresh_token, generate_jwt_token

OTP_LIFETIME=120


class SendVerification(APIView):
    def post(self, request):
        serializer = SendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_200_OK)


class CheckVerification(APIView):
    def post(self, request):
        serializer = CheckVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'OTP verified successfully, email verified.'}, status=status.HTTP_200_OK)

class RegistrationView(APIView):
    def post(self, reuqest):
        serializer = UserSerializer(data=reuqest.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data['access_token']
        refresh_token = serializer.validated_data['refresh_token']

        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=True, samesite='Strict')
        response.data = {
            'access_token': access_token,
        }
        return response


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

class LoginView(APIView):
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




