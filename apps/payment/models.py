from django.db import models

from apps.shared.models import BaseModel
from apps.users.models import User
from apps.rent.models import RentHistory

from apps.shared.enums import PaymentStatusChoices, PaymentMethodChoices, Currencies

import hashlib
from cryptography.fernet import Fernet
from django.conf import settings

class Card(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    four_digits = models.CharField(max_length=4)
    expiry_date = models.CharField(max_length=5) # saqlanmidi
    hashed_cvv = models.CharField(max_length=64) # saqlanmidi
    encrypted_number = models.BinaryField(default=None) # saqlanmidi

    full_number = False
    cvv = False

    def __str__(self):
        return f'{self.user} - **** **** **** {self.four_digits}'

    def save(self, *args, **kwargs):
        if len(self.cvv) <= 4:
            self.hashed_cvv = self.hash_cvv(self.cvv)
            self.encrypted_number = self.encrypt_card_number(self.full_number)
        super().save(*args, **kwargs)

    @staticmethod
    def hash_cvv(cvv):
        return hashlib.sha256(cvv.encode()).hexdigest()

    def encrypt_card_number(self, card_number):
        cipher_suite = Fernet(settings.ENCRYPTION_KEY)
        encrypted_text = cipher_suite.encrypt(card_number.encode())
        return encrypted_text
    
    def decrypt_card_number(self):
        cipher_suite = Fernet(settings.ENCRYPTION_KEY)
        decrypted_key = cipher_suite.decrypt(self.encrypted_number).decode()
        return decrypted_key

    class Meta:
        verbose_name = ('Card')
        verbose_name_plural = ('Cards')

    def set_card_details(self, full_number, cvv):
        self.four_digits = full_number[-4:]
        self.full_number = full_number
        self.cvv = cvv


class Transaction(BaseModel): # change to Base Model later
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




