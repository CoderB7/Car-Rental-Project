from django.db import models

from apps.shared.models import TimeStampedModel
from apps.users.models import User
from apps.cars.models import Car


class RentHistory(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_history')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rent_history')
    rental_start = models.DateField()
    rental_end = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    agreement_signed = models.BooleanField(default=False) # offerta
    
    def __str__(self):
        return f"Rental by {self.user.email} for {self.car.license_plate} from {self.rental_start} to {self.rental_end}"

    class Meta:
        verbose_name = ('Rent History')
        verbose_name_plural = ('Rent History')

