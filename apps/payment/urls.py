from django.urls import path
from apps.payment.api.views import (
    CardCreateRequestView,
    CardGetVerifyCodeView,
    CardVerifyCodeView,
    CardDeleteView
)

urlpatterns = [
    path('card/create_request/', CardCreateRequestView.as_view(), name='card-create-request'),
    path('card/get_verify_code/', CardGetVerifyCodeView.as_view(), name='card-get-verify-code'),
    path('card/verify/', CardVerifyCodeView.as_view(), name='card-verify'),
    path('card/<uuid:id>/', CardDeleteView.as_view(), name='card-delete')
]