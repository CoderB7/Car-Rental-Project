from django.db import models

from apps.shared.enums import BookingStatusChoices
from apps.shared.models import BaseModel
from apps.users.models import User
from apps.cars.models import Car


class RentHistory(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_histories')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rent_histories')
    rental_start = models.DateField()
    rental_end = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    agreement_signed = models.BooleanField(default=False) # offerta
    
    def __str__(self):
        return f"Rental by {self.user.email} for {self.car.license_plate} from {self.rental_start} to {self.rental_end}"

    class Meta:
        db_table = "rent_history"
        verbose_name = ('Rent History')
        verbose_name_plural = ('Rent History')


class Booking(BaseModel): # Booking
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Carts')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='Carts')
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    rental_start = models.DateField()
    rental_end = models.DateField()
    status = models.CharField(max_length=35, choices=BookingStatusChoices.choices(), default=BookingStatusChoices.PENDING.value)

    class Meta:
        db_table = "booking"
        ordering = ['-created_at']
        verbose_name = ('Booking')
        verbose_name_plural = ('Bookings')
    
    def __str__(self):
        return f'Reservation {self.id} for {self.car.name}'