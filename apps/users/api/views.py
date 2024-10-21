import jwt
import datetime

from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .serializers import UserSerializer, UserProfileSerializer, LoginSerializer
from .serializers import SendVerificationSerializer, CheckVerificationSerializer, RefreshTokenSerializer
from apps.shared.redis_client import blacklist_token


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


class CheckVerification(APIView):
    def post(self, request):
        serializer = CheckVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'OTP verified successfully, email verified.'}, status=status.HTTP_200_OK)

class RegistrationView(APIView):
    def post(self, reuqest):
        serializer = UserSerializer(data=reuqest.data)
        serializer.is_valid(raise_exception=True)
        user, access_token, refresh_token = serializer.save()
        access_token = serializer.validated_data['access_token']
        refresh_token = serializer.validated_data['refresh_token']

        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=True, samesite='Strict')
        response.data = {
            'access_token': access_token,
        }
        return response


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                blacklist_token(refresh_token)
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

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data['access_token']
        refresh_token = serializer.validated_data['refresh_token']

        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=True, samesite='Strict')
        response.data = {
            'access_token': access_token,
        }
        return response
        
        
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token', None)
        serializer = RefreshTokenSerializer(data={'refresh_token': refresh_token})
        serializer.is_valid(raise_exception=True)
        new_access_token, new_refresh_token = serializer.create(serializer.validated_data)

        response = Response()
        response.set_cookie(key='refresh_token', value=new_refresh_token, httponly=True, secure=True, samesite='Strict')
        response.data = {
            'access_token': new_access_token,
        }
        response.status_code = status.HTTP_200_OK
        return response

