from django.db import models
from django.contrib.auth.models import AbstractUser
from django_softdelete.models import SoftDeleteModel

from apps.users.managers import UserManager
from apps.shared.models import TimeStampedModel

class User(SoftDeleteModel, AbstractUser, TimeStampedModel):
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

    def delete(self, strict: bool=False, *args, **kwargs):
        super().delete(strict=strict, *args, **kwargs)

        if self.email:
            self.email = f"DELETED_{self.id}_{self.email}"
        # if self.phone:
            # self.phone = f"DELETED_{self.id}_{self.phone}"
        self.save(update_fields=["email", "phone"])
    
    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        # if not self.phone:
            # self.phone = None
        super(User, self).save(*args, **kwargs)


class DriverLicence(TimeStampedModel):
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
