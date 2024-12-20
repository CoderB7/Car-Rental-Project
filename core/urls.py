from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect


from .schema import swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
]

urlpatterns += [
    path("api/users/", include('apps.users.urls')),
    path("api/cars/", include('apps.cars.urls')),
    path("api/rent/", include('apps.rent.urls')),
    path("api/payment/", include('apps.payment.urls')),
]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
