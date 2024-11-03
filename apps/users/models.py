import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.core.exceptions import ValidationError

from apps.users.managers import UserManager
from apps.shared.models import BaseModel
from apps.shared.utils import process_image, process_document
from apps.cars.models import Car


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True, blank=False)

    date_of_birth = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    
    address = models.CharField(max_length=128, null=True, blank=True)
    passport_number = models.CharField(max_length=64)
    passport_file = models.FileField(upload_to='passports/', max_length=255, blank=True, null=True)

    username = None

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        db_table = "user"
        verbose_name = ('User')
        verbose_name_plural = ('Users')

    def save(self, *args, **kwargs):
        if self.passport_file:
            ext = os.path.splitext(self.passport_file.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png']:
                new_filename, processed_image = process_image(self.passport_file, new_width=800, new_height=800)
                new_filename = f"{new_filename.rsplit('.', 1)[0]}_{self.id}.jpg"
                self.passport_file.save(new_filename, processed_image, save=False)
            else:
                new_filename, file = process_document(self.passport_file, self.id)
                self.passport_file.save(new_filename, file, save=False)
        try:
            super().save(*args, **kwargs)   
        except Exception as e:
            print(f"Error in super().save(): {e}")

    def delete(self, *args, **kwargs):
        # check if the file exists and delete it
        if self.passport_file:
            if os.path.isfile(self.passport_file.path):
                os.remove(self.passport_file.path)
        super().delete(*args, **kwargs)
    

class DriverLicence(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='driver_licence')
    
    number = models.CharField(max_length=32, unique=True)
    issuing_state = models.CharField(max_length=64)
    expiry_date = models.DateField()
    image = models.ImageField(upload_to='user/driver_licence/', blank=True, null=True)
    
    def __str__(self):
        return f'{self.user} - {self.number}'

    class Meta:
        db_table = "driver_licence"
        verbose_name = ('Driver Licence')
        verbose_name_plural = ('Driver Licences')


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


class BlacklistedToken(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blacklisted_tokens')
    access_token = models.CharField(max_length=1024, unique=True)
    refresh_token = models.CharField(max_length=1024, unique=True)


    def __str__(self):
        return f"{self.user.first_name}'s blacklisted token"

    @classmethod
    def blacklist_token(cls, user, access, refresh):
        """Blacklists a refresh token."""
        if not cls.is_token_blacklisted(access, refresh):
            cls.objects.get_or_create(user=user, access_token=access, refresh_token=refresh)

    @classmethod
    def is_token_blacklisted(cls, access, refresh):
        """Checks if a refresh token is blacklisted."""
        # Initialize an empty Q object
        query = Q()
        # Conditionally add access token to the query
        if access:
            query |= Q(access_token=access)
        # Conditionally add refresh token to the query
        if refresh:
            query |= Q(refresh_token=refresh)
        # If neither token is provided, return False
        if not query:
            return False
        # Return whether any records match the constructed query
        return cls.objects.filter(query).exists()

    class Meta:
        db_table = "blacklisted_token"
        verbose_name = ('Blacklisted Token')
        verbose_name_plural = ('Blacklisted Tokens')