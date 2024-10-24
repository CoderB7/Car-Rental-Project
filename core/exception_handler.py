from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.exceptions import AuthenticationFailed

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, AuthenticationFailed):
            return Response({
                "success": False,
                "code": response.status_code,
                "message": str(exc),
                "data": {}
            }, status=response.status_code)
        
        elif isinstance(exc, serializers.ValidationError):
            return Response({
                "success": False,
                "code": response.status_code,
                "message": response.data.get('detail', 'Validation error occured'),
                "data": response.data if response.data is not None else {}
            }, status=response.status_code)
    return Response({
        "success": False,
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "An unexpected error occured.",
        "data": {}
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)