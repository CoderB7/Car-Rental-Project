import datetime

from rest_framework import serializers

from django.core.cache import cache
from django.conf import settings

from ..models import User
from .utils import generate_otp, is_otp_unique, send_otp_via_email, decrypt_access_token, decrypt_refresh_token, generate_jwt_token


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class SendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value
    
    def validate(self, data):
        email = data.get('email', None)

        otp = generate_otp()
        while not is_otp_unique(email, otp):
            otp = generate_otp()
        
        cache.set(f"{email}", otp, timeout=600)
        send_otp_via_email(email, otp)

        return data


class CheckVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    email_verify = serializers.BooleanField(read_only=True)  # Field to explicitly communicate the verification status
    
    def validate_otp(self, value):
        email = self.initial_data.get('email', None)
        cached_otp = cache.get(f'{email}')
        print(type(cached_otp))
        if not cached_otp:
            raise serializers.ValidationError('OTP expired or not found')
        if value != cached_otp:
            print('hello')
            raise serializers.ValidationError('Invalid OTP')
        return True
    
    def validate(self, data):
        email =  data.get('email', None)

       
        self.email_verify = True
        
        cache.delete(f"{email}")
        cache.set(f"{email}_verify", self.email_verify, timeout=float(settings.OTP_LIFETIME))

        return data


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate_password(self, password):
        if not password:
            raise serializers.ValidationError('Password is required')
        return password

    def create_user_and_tokens(self, email, password, first_name, last_name):
        user = User.objects.create_user(
            email, 
            password, 
            first_name=first_name, 
            last_name=last_name,
        )
        payload = {
            'user_id': user.id,
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }
        # Convert datetime to Unix timestamps
        payload['iat'] = int(payload['iat'].timestamp())
        access_token, refresh_token = generate_jwt_token(payload)
        return user, access_token, refresh_token

    def validate(self, attrs):
        email = attrs.get('email', None)
        first_name = attrs.get('first_name', None)
        last_name = attrs.get('last_name', None)
        password = attrs.get('password', None)

        is_email_valid = cache.get(f'{email}_verify')
        if not is_email_valid:
            raise serializers.ValidationError('Email is not valid')
        
        self.validate_password(password)
        user, access_token, refresh_token = self.create_user_and_tokens(email, password, first_name, last_name)
        attrs['user'] = user
        attrs['access_token'] = access_token
        attrs['refresh_token'] = refresh_token
        
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
        )
    
    
class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    
