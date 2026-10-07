from decimal import Decimal
from random import choice, randint

from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Product


PRODUCT_NAMES = [
    "Фільтр масла", "Гальмівні колодки", "Повітряний фільтр",
    "Свічка запалювання", "Акумулятор", "Ремінь ГРМ",
    "Амортизатор", "Паливний насос", "Радіатор охолодження", "Фара передня",
]

VEHICLE_BRANDS = [
    "Toyota", "Volkswagen", "Ford", "Honda", "BMW",
    "Renault", "Nissan", "Hyundai", "Skoda", "Mazda",
]

COUNTRIES = [
    "Japan", "Germany", "USA", "France", "South Korea",
    "Czech Republic", "Italy", "Poland",
]


def generate_product():
    brand = choice(VEHICLE_BRANDS)
    prefix = brand[:2].upper()
    return Product(
        name=choice(PRODUCT_NAMES),
        vehicle_brand=brand,
        part_number=f"{prefix}-{randint(1000, 9999)}-{randint(10, 99)}",
        origin_country=choice(COUNTRIES),
        price=Decimal(randint(20000, 500000)) / Decimal("100"),
    )


def products_list(request):
    products = Product.objects.all().order_by("id")
    return render(
        request,
        "catalog/products.html",
        {
            "products": products,
            "title": "Склад автозапчастин",
        },
    )


def products(request):
    return products_list(request)


def replenish(request, count):
    if count < 1:
        messages.error(request, "Кількість має бути більшою за 0.")
        return redirect("products_list")

    new_products = [generate_product() for _ in range(count)]
    Product.objects.bulk_create(new_products)
    messages.success(request, f"Успішно згенеровано та додано {count} нових товарів!")
    return redirect("products_list")
