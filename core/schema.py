from django.urls import re_path, path
from django.contrib.auth.mixins import LoginRequiredMixin
from drf_spectacular import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import permissions

from drf_spectacular.generators import BaseSchemaGenerator
from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from core.authentication import CustomJWTAuthentication


class SecureSwaggerView(LoginRequiredMixin, SpectacularSwaggerView):
    login_url = '/admin/'


swagger_urlpatterns = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SecureSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    re_path(r'^swagger/$', SecureSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]


class CustomJWTAuthenticationExtension(SimpleJWTScheme):
    target_class = CustomJWTAuthentication
    name = 'CustomJWT'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'schema': 'bearer',
            'bearerFormat': 'JWT',
        }
    

class BothHttpAndHttpsSchemaGenerator(BaseSchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema

# re_path(r'^swagger/$', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
# re_path(r'^swagger(?P<format>\.json|\.yaml)$', SpectacularAPIView.as_view(), name='schema-json'),
# re_path(r'^redoc/$', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Car Rental API",
#         default_version="v1",
#         description="Car Rental Group",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="info@carrental.group"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     generator_class=BothHttpAndHttpsSchemaGenerator,
#     permission_classes=(permissions.AllowAny,),
# )
# swagger_urlpatterns = [
#     re_path(
#         r"^swagger(?P<format>\.json|\.yaml)$",
#         schema_view.without_ui(cache_timeout=0),
#         name="schema-json",
#     ),
#     re_path(
#         r"^swagger/$",
#         schema_view.with_ui("swagger", cache_timeout=0),
#         name="schema-swagger-ui",
#     ),
#     re_path(
#         r"^redoc/$",
#         schema_view.with_ui("redoc", cache_timeout=0),
#         name="schema-redoc",
#     ),
# ]
