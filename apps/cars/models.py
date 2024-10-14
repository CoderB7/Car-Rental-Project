from django.db import models

from apps.shared.models import BaseModel

class Brand(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    origin = models.CharField(max_length=64, null=True, blank=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    year = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    # def save(*args, **kwargs):
    #     if self.logo:
            
    
    class Meta:
        verbose_name = ('Brand')
        verbose_name_plural = ('Brands')


class Car(BaseModel):
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

    license_plate = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=64)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, related_name='car')
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
        return f'{self.name} - {self.brand.name}' # add brand also
    
    class Meta:
        verbose_name = ('Car')
        verbose_name_plural = ('Cars')
        


