from enum import Enum


class EnumBaseModel(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class UserRoleChoices(EnumBaseModel):
    SUPER_ADMIN = "super_admin"
    COMPANY_ADMIN = "company_admin"
    STAFF = "staff"
    USER = "user"

class TransmissionChoices(EnumBaseModel):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    

class FuelTypeChoices(EnumBaseModel):
    PETROL = "petrol"
    HYBRID = "hybrid"
    ELECTRIC = "electric"


class CarTypeChoices(EnumBaseModel):
    SEDAN = "sedan"
    COUPE = "coupe"
    SUV = "suv"
    SPORTSCAR = "sportscar"
    CROSSOVER = "crossover"
    PICKUP_TRUCK = "pickup_truck"
    LIMOUSINE = "limousine"


class PaymentStatusChoices(EnumBaseModel):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Currencies(EnumBaseModel):
    UZS = "uzs"
    USD = "usd"
    EUR = "eur"


class PaymentMethodChoices(EnumBaseModel):
    CASH = "cash"
    CARD = "card"


class BookingStatusChoices(EnumBaseModel):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    EXPIRED = "expired"
