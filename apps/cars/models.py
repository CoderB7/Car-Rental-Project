from django.db import models

from apps.shared.models import TimeStampedModel

class Car(TimeStampedModel):
    class TransmissionChoices(models.TextChoices):
        MANUAL = ('manual', 'Manual') # 0->database, 1->for user
        AUTOMATIC = ('automatic', 'Automatic')

    class FuelTypeChoices(models.TextChoices):
        PETROL = ('petrol', 'Petrol')
        HYBRID = ('hybrid', 'Hybrid')
        ELECTRIC = ('electric', 'Electric')

    class CarTypeChoices(models.TextChoices):
        SEDAN = ('sedan', 'Sedan')
        COUPE = ('coupe', 'Coupe')
        SUV = ('suv', 'SUV')
        SPORTSCAR = ('sportscar', 'Sportscar')
        CROSSOVER = ('crossover', 'Crossover')
        PICKUP_TRUCK = ('pickup_truck', 'Pickup Truck')
        LIMOUSINE = ('limuosine', 'Limousine')

    name = models.CharField(max_length=64)
    transmission = models.CharField(
        max_length=12,
        choices=TransmissionChoices.choices,
        default=TransmissionChoices.MANUAL.value,
    )
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    mileage = models.IntegerField()
    doors = models.IntegerField()
    seats = models.IntegerField()
    fuel_type = models.CharField(
        max_length=12,
        choices=FuelTypeChoices.choices,
        default=FuelTypeChoices.PETROL.value,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    type = models.CharField(
        max_length=24,
        choices=CarTypeChoices.choices,
        default=CarTypeChoices.SEDAN.value,
    )
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return f'{self.name}' # add brand also
    
    class Meta:
        verbose_name = ('Car')
        verbose_name_plural = ('Cars')
        
