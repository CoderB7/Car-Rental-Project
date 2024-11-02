from celery import shared_task
from django.utils import timezone
from apps.rent.models import Booking


@shared_task
def expire_old_bookings():
    expiration_time = timezone.now() - timezone.timedelta(hours=24) # hours = 24
    expired_bookings = Booking.objects.filter(status='pending', created_at__lt=expiration_time)
    expired_bookings.update(status='expired')
    

