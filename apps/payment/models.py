from django.db import models

from apps.shared.models import TimeStampedModel
from apps.users.models import User
from apps.rent.models import RentHistoy

class Card(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.user} - {self.number}'

    class Meta:
        verbose_name = ('Card')
        verbose_name_plural = ('Cards')


class Transaction(TimeStampedModel):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = ('pending', 'Pending') # 0->database, 1->for user
        COMPLETED = ('completed', 'Completed')
        FAILED = ('failed', 'Failed')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    rental = models.ForeignKey(RentHistoy, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=12,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING.value,
    )
    currency = models.CharField(max_length=3, default='USD')
    card = models.OneToOneField(Card, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.amount}'
    
    class Meta:
        verbose_name = ('Payment')
        verbose_name_plural = ('Payments')




