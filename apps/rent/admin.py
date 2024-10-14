from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import RentHistory


@admin.register(RentHistory)
class RentHistoryAdmin(ModelAdmin):
    fieldsets = (
        (None, {"fields": ("user", "car")}),
        ("Rent info", {"fields": ("rental_start", "rental_end", "total_cost")}),
        ("Address", {"fields": ("pickup_location", "dropoff_location")}), 
        ("Agreement signed", {"fields": ("agreement_signed", )})
    )
    list_display = ("id", "user", "car", "rental_start", "rental_end")
    list_display_links = ("id", "user", "car")
    list_filter = ("rental_start", "rental_end")
    search_fields = ("user", "car",)
    ordering = ("-id", )
