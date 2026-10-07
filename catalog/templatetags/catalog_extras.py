from decimal import Decimal

from django import template

from catalog.models import Product

register = template.Library()


@register.filter(name="uah")
def uah(value):
    if value is None or value == "":
        return "0.00 грн."
    try:
        if isinstance(value, str):
            num = Decimal(value)
        else:
            num = Decimal(str(value))
        formatted = f"{num:,.2f}".replace(",", " ")
        return f"{formatted} грн."
    except Exception:
        return f"{value} грн."


@register.simple_tag
def product_count():
    return Product.objects.count()
