from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MasterProfile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(MasterProfile)
class MasterProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "city", "created_at")
    search_fields = ("display_name", "user__username", "city")
    list_filter = ("city",)
