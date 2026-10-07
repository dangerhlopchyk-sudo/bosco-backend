from decimal import Decimal, InvalidOperation
from random import choice, randint

from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Product


PRODUCT_NAMES = [
    "Фільтр масла",
    "Гальмівні колодки",
    "Повітряний фільтр",
    "Свічка запалювання",
    "Акумулятор",
    "Ремінь ГРМ",
    "Амортизатор",
    "Паливний насос",
    "Радіатор охолодження",
    "Фара передня",
]

VEHICLE_BRANDS = [
    "Toyota",
    "Volkswagen",
    "Ford",
    "Honda",
    "BMW",
    "Renault",
    "Nissan",
    "Hyundai",
    "Skoda",
    "Mazda",
]

COUNTRIES = [
    "Japan",
    "Germany",
    "USA",
    "France",
    "South Korea",
    "Czech Republic",
    "Italy",
    "Poland",
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


def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        vehicle_brand = request.POST.get("vehicle_brand", "").strip()
        part_number = request.POST.get("part_number", "").strip()
        origin_country = request.POST.get("origin_country", "").strip()
        price_raw = request.POST.get("price", "").strip()

        if not (name and vehicle_brand and part_number and origin_country and price_raw):
            messages.error(request, "Будь ласка, заповніть усі обов'язкові поля.")
            return render(
                request,
                "catalog/add_product.html",
                {
                    "title": "Додати автозапчастину",
                    "form_data": request.POST,
                },
            )

        try:
            price = Decimal(price_raw.replace(",", "."))
            if price <= 0:
                raise ValueError("Ціна має бути більшою за 0")
        except (InvalidOperation, ValueError):
            messages.error(request, "Вкажіть коректну ціну (додатнє число).")
            return render(
                request,
                "catalog/add_product.html",
                {
                    "title": "Додати автозапчастину",
                    "form_data": request.POST,
                },
            )

        product = Product.objects.create(
            name=name,
            vehicle_brand=vehicle_brand,
            part_number=part_number,
            origin_country=origin_country,
            price=price,
        )
        messages.success(
            request,
            f'Товар "{product.name}" ({product.part_number}) успішно додано до складу!',
        )
        return redirect("products_list")

    return render(
        request,
        "catalog/add_product.html",
        {
            "title": "Додати автозапчастину",
        },
    )


def replenish(request, count):
    if count < 1:
        messages.error(request, "Кількість має бути більшою за 0.")
        return redirect("products_list")

    new_products = [generate_product() for _ in range(count)]
    Product.objects.bulk_create(new_products)
    messages.success(request, f"Успішно згенеровано та додано {count} нових товарів!")
    return redirect("products_list")
