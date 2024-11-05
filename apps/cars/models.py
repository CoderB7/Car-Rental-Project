import os

from django.db import models
from tempfile import NamedTemporaryFile
from rest_framework import status

from apps.users.models import User
from apps.shared.models import BaseModel
from apps.shared.enums import TransmissionChoices, FuelTypeChoices, CarTypeChoices
from apps.shared.utils import process_image, process_logo

class Brand(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    origin = models.CharField(max_length=64, null=True, blank=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    year = models.IntegerField()
    
    class Meta:
        db_table = "brand"
        verbose_name = ('Brand')
        verbose_name_plural = ('Brands')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.logo:
            new_filename, processed_logo = process_logo(self.logo, new_width=400, new_height=400)
            self.logo.save(new_filename, processed_logo, save=False)
        
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error in super().save(): {e}")

    def delete(self, *args, **kwargs):
        if self.logo:
            if os.path.isfile(self.logo.path):
                os.remove(self.logo.path)
        super().delete(*args, **kwargs)


class Car(BaseModel):
    license_plate = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=64)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, related_name='car')
    transmission = models.CharField(max_length=25, choices=TransmissionChoices.choices(), default=TransmissionChoices.MANUAL.value)
    year = models.IntegerField()
    color = models.CharField(max_length=40)
    mileage = models.IntegerField()
    doors = models.IntegerField()
    seats = models.IntegerField()
    fuel_type = models.CharField(max_length=25, choices=FuelTypeChoices.choices(), default=FuelTypeChoices.PETROL.value)
    price = models.FloatField()
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    type = models.CharField(max_length=25, choices=CarTypeChoices.choices(), default=CarTypeChoices.SEDAN.value)
    rating = models.FloatField()
    
    class Meta:
        db_table = "car"
        verbose_name = ('Car')
        verbose_name_plural = ('Cars')
        
    def __str__(self):
        return f'{self.name} - {self.brand.name}'
    
    def save(self, *args, **kwargs):
        if self.image:
            new_filename, processed_image = process_image(self.image, new_width=800, new_height=800)
            # Save the BytesIO object to the ImageField with the new filename
            self.image.save(new_filename, processed_image, save=False)
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error in super().save(): {e}") 

    def delete(self, *args, **kwargs):
        # Check if the image exists and delete it
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


class Review(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()

    def __str__(self):
        return f'Review by {self.user.email} for {self.car.license_plate}'

    class Meta:
        db_table = "review"
        verbose_name = ('Review')
        verbose_name_plural = ('Reviews')