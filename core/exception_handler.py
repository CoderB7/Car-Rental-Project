import logging

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

logging.basicConfig(level=logging.INFO)

def custom_exception_handler(exc:BaseException, context:dict)->Response:
    response = exception_handler(exc, context)
    
    if response is None:
        return Response({
        "success": False,
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "An unexpected error occured.",
        "data":  {'detail':str(exc)}
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    request:Request = context.get('request')

    if isinstance(exc, NotAuthenticated):
        is_swagger_view:bool= "swagger" in request.get_full_path()
        logging.info(f"NotAuthenticated exc. occurred -> {exc=}")
        return (
            Response({
                "success": False,
                "code": response.status_code,
                "message": str(exc),
                "data": {}
            }, status=response.status_code) 
            if not is_swagger_view else 
            response
        )
    
    elif isinstance(exc, AuthenticationFailed):
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
            "message": response.data,
            "data": {}
        }, status=response.status_code)

    return response