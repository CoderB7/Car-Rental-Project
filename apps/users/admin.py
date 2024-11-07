from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.contrib.auth.models import User, Group

from unfold.admin import ModelAdmin

from .models import User, DriverLicence, BlacklistedToken, Review

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm 
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "address", "role")}),
        ("Passport info", {"fields": ("passport_number", "passport_file")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("id", "email", "first_name", "last_name", "is_staff")
    list_display_links = ("id", "email")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email", "first_name", "last_name")
    filter_horizontal = ("groups", "user_permissions")
    ordering = ("-id",)
    # readonly_fields = ("last_login", "date_joined", "created_at", "updated_at")


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(DriverLicence)
class DriverLicenceAdmin(ModelAdmin):
    list_display = ('id', 'user', 'number', 'issuing_state', 'expiry_date')
    fieldsets = (
        ('User', { 'fields': ('user',)}),
        ('Licence Details', { 'fields': ('number', 'issuing_state', 'expiry_date', 'image')}),
    )
    search_fields = ('user', 'number', 'expiry_date')
    ordering = ('-id',)


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


@admin.register(BlacklistedToken)
class BlacklistedTokenAdmin(ModelAdmin):
    fieldsets = (
        (None, {"fields": ("user", "access_token", "refresh_token")}),
    )
    list_display = ("id", "user", "access_token", "refresh_token")
    list_display_links = ("id", "user")
    search_fields = ("user", )
    ordering = ("-id", )

