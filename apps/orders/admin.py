from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("title", "price", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "status", "total", "created_at", "paid_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "buyer__username", "full_name")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at", "paid_at", "total")
