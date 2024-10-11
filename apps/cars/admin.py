from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Car

@admin.register(Car)
class CarAdmin(ModelAdmin):
    fieldsets = (
        ("Car Model", {"fields": ("name", "type", )}),# add brand
        ("Car Info", {"fields": ("transmission", "year" "mileage", "fuel_type", "rating", "price")}),
        ("Car Exterior", {"fields": ("color", "image")}),
        ("Car Interior", {"fields": ("doors", "seats")}),
    )
    list_display = ("id", "name", "", "type", "rating", "price") # add brand
    list_filter = ("type", "fuel_type", "transmission")
    search_fields = ("name", "year", "") # add brand
    ordering = ("-id", "rating")

