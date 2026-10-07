from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "vehicle_brand", "part_number", "origin_country", "price")
    search_fields = ("name", "vehicle_brand", "part_number")
    list_filter = ("vehicle_brand", "origin_country")
