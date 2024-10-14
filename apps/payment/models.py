from django.db import models

from apps.shared.models import BaseModel
from apps.users.models import User
from apps.rent.models import RentHistory

from apps.shared.enums import PaymentStatusChoices, PaymentMethodChoices, Currencies

# correct this do not store full number only last 4 digit, hash cvv
class Card(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.user} - {self.number}'

    class Meta:
        verbose_name = ('Card')
        verbose_name_plural = ('Cards')


class Transaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    rental = models.ForeignKey(RentHistory, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=25, choices=PaymentMethodChoices.choices(), default=PaymentMethodChoices.CASH.value)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=25, choices=PaymentStatusChoices.choices(), default=PaymentStatusChoices.PENDING.value)
    currency = models.CharField(max_length=25, choices=Currencies.choices(), default=Currencies.UZS.value)
    card = models.OneToOneField(Card, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.amount}'
    
    class Meta:
        verbose_name = ('Payment')
        verbose_name_plural = ('Payments')




