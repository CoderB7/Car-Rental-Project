from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message="Success", code=status.HTTP_200_OK):
    return Response({
        "success": True, 
        "code": code,
        "message": message,
        "data": data if data is not None else {}
    }, status=code)

def error_response(data=None, message="Error", code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "success": False, 
        "code": code, 
        "message": message,
        "data": data if data is not None else {}
    }, status=code)


