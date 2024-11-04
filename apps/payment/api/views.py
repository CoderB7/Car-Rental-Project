from rest_framework import generics, permissions

from django.shortcuts import get_object_or_404

from apps.shared.utils import success_response, error_response
from ..models import Card, Transaction
from .serializers import (
    CardCreateRequestSerializer,
    CardGetVerifyCodeSerializer,
    CardVerifyCodeSerializer,
    CardDeleteSerializer,
    CardListSerializer
)


class CardCreateRequestView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CardCreateRequestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully sent create request',
        )


class CardGetVerifyCodeView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CardGetVerifyCodeSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Successfully sent get verify code',
        )


class CardVerifyCodeView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CardVerifyCodeSerializer

    def create(self, request):
        user_id = self.request.user.id
        serializers = self.get_serializer(data=request.data, user_id=user_id)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return success_response(
            message='Successfully verified card',
        )


class CardListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CardListSerializer

    def get_queryset(self):
        return Card.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='List of Cards'
        )


class CardDeleteView(generics.DestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardDeleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        card_uuid = kwargs.get('id')
        serializer = self.get_serializer(data={'id': card_uuid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message='Card deleted successfully')

