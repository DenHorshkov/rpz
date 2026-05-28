from django.contrib import admin

from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "price", "stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title", "description")
    inlines = [ProductImageInline]
    prepopulated_fields = {"slug": ("title",)}
