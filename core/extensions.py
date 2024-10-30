# from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from core.authentication import CustomJWTAuthentication


class CustomJWTAuthenticationExtension(SimpleJWTScheme):
    target_class = CustomJWTAuthentication
    name = 'CustomJWT'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'schema': 'bearer',
            'bearerFormat': 'JWT',
        }
