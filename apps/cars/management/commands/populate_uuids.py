import uuid
from django.core.management.base import BaseCommand
from apps.cars.models import Brand, Car
from apps.payment.models import Transaction, Card
from apps.rent.models import RentHistory
from apps.users.models import User, Review, DriverLicence

class Command(BaseCommand):
    help = 'Populate UUIDs for existing records'

    def handle(self, *args, **options):
        for model in [Car, Brand, Transaction, Card, RentHistory, User, Review, DriverLicence]:
            items = model.objects.all()
            for item in items:
                if item.uuid == None:
                    item.uuid = uuid.uuid4()
                    item.save(update_fields=['uuid'])
        self.stdout.write(self.style.SUCCESS('Successfully populated UUIDS for existing records'))   
