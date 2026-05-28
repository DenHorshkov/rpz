from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("seller", "author", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("seller__display_name", "author__username", "text")
