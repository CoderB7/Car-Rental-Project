from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.users.managers import UserManager
from apps.shared.models import BaseModel
from apps.cars.models import Car

class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True, blank=False)

    date_of_birth = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    
    address = models.CharField(max_length=128, null=True, blank=True)
    passport_number = models.CharField(max_length=64)
    passport_file = models.FileField(upload_to='user/passports/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = ('User')
        verbose_name_plural = ('Users')


class DriverLicence(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='driver_licence')
    
    number = models.CharField(max_length=32, unique=True)
    issuing_state = models.CharField(max_length=64)
    expiry_date = models.DateField()
    image = models.ImageField(upload_to='user/driver_licence/', blank=True, null=True)
    
    def __str__(self):
        return f'{self.user} - {self.number}'

    class Meta:
        verbose_name = ('Driver Licence')
        verbose_name_plural = ('Driver Licences')


class Review(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()

    def __str__(self):
        return f'Review by {self.user.email} for {self.car.license_plate}'

    class Meta:
        verbose_name = ('Review')
        verbose_name_plural = ('Reviews')