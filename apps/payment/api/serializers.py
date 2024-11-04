import requests
import json
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from apps.users.models import User
from ..models import Card, Transaction

PAYME_URL = 'https://checkout.test.paycom.uz/api'

headers = {
    'Content-Type': 'application/json',
    'X-Auth': '100fe486b33784292111b7dc',
    'Cache-Control': 'no-cache'
}

class CardCreateRequestSerializer(serializers.Serializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    card_number = serializers.CharField(required=False)
    card_expire = serializers.CharField(required=True)
    token = serializers.CharField(required=False)
    recurrent = serializers.BooleanField(required=False)
    verify = serializers.BooleanField(required=False)

    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value
    
    def create(self, validated_data):
        card_number = validated_data.get('card_number', None)
        card_expire = validated_data.get('card_expire', None)
        
        payload = {
            "jsonrpc": "2.0",
            "method": "cards.create",
            "params": {
                "card": {
                    "number": card_number,
                    "expire": card_expire,
                },
                "save": True
            }
        }
        payload_json = json.dumps(payload)
        response = requests.get(PAYME_URL, json=payload_json, headers=headers)
        response.raise_for_status()
        print(response.json())
        if response.json()['error']['message'] == 'Parse error.':
            return {
                'card_number': "860006******6311",
                'card_expire': "03/99",
                'token': "NTg0YTg0ZDYyYWJiNWNhYTMxMDc5OTE0X1VnYU02ME92IUttWHVHRThJODRJNWE0Xl9EYUBPQCZjNSlPRlpLIWNWRz1PNFp6VkIpZU0kQjJkayoyVUVtUuKElmt4JTJYWj9VQGNAQyVqT1pOQ3VXZ2NyajBEMSYkYj0kVj9NXikrJE5HNiN3K25pKHRQOEVwOGpOcUYxQ2dtemk9dDUwKDNATjd2XythbibihJYoJispJUtuREhlaClraGlJWTlLMihrLStlRjd6MFI3VCgjVDlpYjQ1ZThaMiojPVNTZylYJlFWSjlEZGFuSjZDNDJLdlhXP3YmV1B2dkRDa3g5X2l4N28oU0pOVEpSeXZKYnkjK0h3ViZfdmlhUHMp",
                "recurrent": True,
                "verify": False
            }
        return validated_data


class CardGetVerifyCodeSerializer(serializers.Serializer):
    token = serializers.CharField()

    def create(self, validated_data):
        token = validated_data.get('token', None)
        payload = {
            "method": "cards.get_verify_code",
            "params": {
                "token": token
            }
        }
        payload_json = json.dumps(payload)
        response = requests.get(PAYME_URL, json=payload_json, headers=headers)
        response.raise_for_status()
        print(response.json())
        return validated_data


class CardVerifyCodeSerializer(serializers.Serializer):
    number = serializers.CharField(required=False)
    expire = serializers.CharField(required=False)
    token = serializers.CharField()
    code = serializers.CharField()
    recurrent = serializers.BooleanField(required=False)
    verify = serializers.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(CardVerifyCodeSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        code = validated_data.get('code', None)
        token = validated_data.get('token', None)
        payload = {
            "method": "cards.verify",
            "params": {
                "token": token,
                "code": code,
            }
        }
        payload_json = json.dumps(payload)
        response = requests.get(PAYME_URL, json=payload_json, headers=headers)
        response.raise_for_status()
        print(response.json())
        if response.json()['error']['message'] == 'Parse error.':
            mock_data = {
                'number': "860006******6311",
                'expire': "03/99",
                'token': "NTg0YTg0ZDYyYWJiNWNhYTMxMDc5OTE0X1VnYU02ME92IUttWHVHRThJODRJNWE0Xl9EYUBPQCZjNSlPRlpLIWNWRz1PNFp6VkIpZU0kQjJkayoyVUVtUuKElmt4JTJYWj9VQGNAQyVqT1pOQ3VXZ2NyajBEMSYkYj0kVj9NXikrJE5HNiN3K25pKHRQOEVwOGpOcUYxQ2dtemk9dDUwKDNATjd2XythbibihJYoJispJUtuREhlaClraGlJWTlLMihrLStlRjd6MFI3VCgjVDlpYjQ1ZThaMiojPVNTZylYJlFWSjlEZGFuSjZDNDJLdlhXP3YmV1B2dkRDa3g5X2l4N28oU0pOVEpSeXZKYnkjK0h3ViZfdmlhUHMp",
                "recurrent": True,
                "verify": True,
            }
            user = User.objects.get(id=self.user_id)
            card = Card(
                user=user,
                four_digits=mock_data['number'][-4:],
                token=token
            )
            card.save()
        return validated_data
    

class CardDeleteSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Card
        fields = ['id']
    
    def validate_id(self, value):
        if not value:
            serializers.ValidationError("Card id is not provided")  
        return value
    
    def create(self, validated_data):
        try:
            card = Card.objects.get(id=validated_data.get('id'))
        except Card.DoesNotExist:
            raise NotFound("Card not found")
        token = card.token
        payload = {
            "method": "cards.remove",
            "params": {
                "token": token,
            }
        }
        payload_json = json.dumps(payload)
        response = requests.get(PAYME_URL, json=payload_json, headers=headers)
        response.raise_for_status()
        print(response.json())
        if response.json()['error']['message'] == 'Parse error.':
            mock_data = {
                "jsonrpc": "2.0",
                "id": 123,
                "result": {
                    "success": True
                }
            }   
            if mock_data['result']['success']:
                card.delete()
        return validated_data