from django.urls import re_path, path
#from drf_yasg import openapi
#from drf_yasg.views import get_schema_view
from drf_spectacular import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import permissions

from .generator import BothHttpAndHttpsSchemaGenerator

swagger_urlpatterns = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    re_path(r'^swagger/$', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
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
