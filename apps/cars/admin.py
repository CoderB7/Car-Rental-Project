from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Car, Brand, Review

@admin.register(Car)
class CarAdmin(ModelAdmin):
    fieldsets = (
        ("Car Model", {"fields": ("name", "brand", "type")}),#
        ("Car Info", {"fields": ("license_plate", "transmission", "year", "mileage", "fuel_type", "rating", "price")}),
        ("Car Exterior", {"fields": ("color", "image")}),
        ("Car Interior", {"fields": ("doors", "seats")}),
    )
    list_display = ("id", "license_plate", "name", "type", "rating", "price") 
    list_filter = ("type", "fuel_type", "transmission")
    search_fields = ("name", "year", "brand")
    ordering = ("-id", "rating")

@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    fieldsets = (
        ("Brand", {"fields": ("name", "origin", "year", "logo")}),
    )
    list_display = ("id", "name", "origin", "year")
    list_filter = ("year",)
    search_fields = ("name", "origin", "year")
    ordering = ("-id",)

@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    fieldsets = (
        (None, {"fields": ("user", "car", "rating", "comment")}),
    )
    list_display = ("id", "user", "car", "rating")
    list_display_links = ("id", "user", "car")
    list_filter = ("rating",)
    search_fields = ("user", "car")
    ordering = ("-id", )
