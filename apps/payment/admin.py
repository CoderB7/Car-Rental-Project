from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Card, Transaction

@admin.register(Card)
class CardAdmin(ModelAdmin):
    fieldsets = (
        ("Card info", {"fields": ("user", "four_digits", "expiry_date", "hashed_cvv")}),
    )
    list_display = ("id", "user", "four_digits")
    list_display_links = ("id", "user")
    list_filter = ("expiry_date", )
    search_fields = ("number", )
    ordering = ("-id",)


@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    fieldsets = (
        (None, {"fields": ("user", "rental")}), 
        ("Transaction info", {"fields": ("amount", "payment_date", "payment_method", "transaction_id", "status")}),
        ("Card info", {"fields": ("currency", "card")}),
    )
    list_display = ("id", "user", "rental", "amount", "payment_date", "status") # add rental
    list_display_links = ("id", "user", "rental") 
    list_filter = ("currency", )
    search_fields = ("user", "transaction_id",)
    ordering = ("-id",) # descending order


