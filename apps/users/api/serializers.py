import datetime

from rest_framework import serializers

from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import authenticate

from ..models import User
from .utils import generate_otp, is_otp_unique, send_otp_via_email, decrypt_access_token, decrypt_refresh_token, generate_jwt_token
from apps.shared.redis_client import (
    set_otp, 
    get_otp, 
    delete_otp,
    set_verify, 
    get_verify,
)

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
        
        # cache.set(f"{email}", otp, timeout=600)
        set_otp(email, otp)
        send_otp_via_email(email, otp)

        return data


class CheckVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    email_verify = serializers.BooleanField(read_only=True)  # Field to explicitly communicate the verification status
    
    def validate_otp(self, value):
        email = self.initial_data.get('email', None)
        # cached_otp = cache.get(f'{email}')
        cached_otp = get_otp(email)
        if not cached_otp:
            raise serializers.ValidationError('OTP expired or not found')
        if value != cached_otp:
            print('hello')
            raise serializers.ValidationError('Invalid OTP')
        return True
    
    def validate(self, data):
        email =  data.get('email', None)
        self.email_verify = True
        delete_otp(email)
        # cache.delete(f"{email}")
        # cache.set(f"{email}_verify", self.email_verify, timeout=float(settings.OTP_LIFETIME))
        set_verify(email, self.email_verify)
        return data


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(required=False)
    
    def validate_password(self, password):
        if not password:
            raise serializers.ValidationError('Password is required')
        return password

    def create_user_and_tokens(self, email, password, first_name, last_name, dob):
        user = User.objects.create_user(
            email, 
            password, 
            first_name=first_name, 
            last_name=last_name,
            date_of_birth=dob,
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
        date_of_birth = attrs.get('date_of_birth', None)

        # is_email_valid = cache.get(f'{email}_verify')
        is_email_valid = get_verify(email)
        if not is_email_valid:
            raise serializers.ValidationError('Email is not valid')
        
        self.validate_password(password)
        user, access_token, refresh_token = self.create_user_and_tokens(email, password, first_name, last_name, date_of_birth)
        attrs['user'] = user
        attrs['access_token'] = access_token
        attrs['refresh_token'] = refresh_token
        
        return attrs
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create_tokens(self, user):
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
        password = attrs.get('password', None)

        user = authenticate(username=email, password=password)
        if user is not None:
            user, access_token, refresh_token = self.create_tokens(user)
            attrs['user'] = user
            attrs['access_token'] = access_token
            attrs['refresh_token'] = refresh_token
        else:
            raise serializers.ValidationError('Invalid email or password.')

        return attrs
    

class UserProfileSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    date_of_birth = serializers.DateField()

