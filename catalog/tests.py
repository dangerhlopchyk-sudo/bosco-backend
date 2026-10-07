from decimal import Decimal

from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Product
from catalog.templatetags.catalog_extras import product_count, uah


class ProductModelTest(TestCase):
    def test_product_str(self):
        product = Product.objects.create(
            name="Фільтр масла",
            vehicle_brand="Toyota",
            part_number="TY-OF-1001",
            origin_country="Japan",
            price=Decimal("420.00"),
        )
        self.assertEqual(str(product), "Фільтр масла (TY-OF-1001)")


class TemplateTagsAndFiltersTest(TestCase):
    def test_uah_filter(self):
        self.assertEqual(uah(1350.50), "1 350.50 грн.")
        self.assertEqual(uah("4200.00"), "4 200.00 грн.")
        self.assertEqual(uah(0), "0.00 грн.")
        self.assertEqual(uah(None), "0.00 грн.")
        self.assertEqual(uah(""), "0.00 грн.")

    def test_product_count_tag(self):
        self.assertEqual(product_count(), 0)
        Product.objects.create(
            name="Свічка запалювання",
            vehicle_brand="Honda",
            part_number="HN-SP-4408",
            origin_country="Japan",
            price=Decimal("260.00"),
        )
        self.assertEqual(product_count(), 1)


class CatalogViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name="Гальмівні колодки",
            vehicle_brand="Volkswagen",
            part_number="VW-BP-2040",
            origin_country="Germany",
            price=Decimal("1350.50"),
        )

    def test_products_list_view_success(self):
        response = self.client.get(reverse("products_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/products.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "partials/menu.html")
        self.assertContains(response, "Гальмівні колодки")
        self.assertContains(response, "VW-BP-2040")
        self.assertContains(response, "1 350.50 грн.")

    def test_products_list_empty_state(self):
        Product.objects.all().delete()
        response = self.client.get(reverse("products_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Товарів немає")

    def test_xss_autoescaping(self):
        Product.objects.create(
            name="<script>alert(1)</script>",
            vehicle_brand="BMW",
            part_number="BM-TEST-01",
            origin_country="Germany",
            price=Decimal("999.00"),
        )
        response = self.client.get(reverse("products_list"))
        self.assertEqual(response.status_code, 200)
        # Verify that <script> was converted to HTML entities and NOT rendered raw
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertNotContains(response, "<script>alert(1)</script>")

    def test_add_product_get(self):
        response = self.client.get(reverse("add_product"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/add_product.html")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_add_product_post_valid(self):
        payload = {
            "name": "Акумулятор",
            "vehicle_brand": "BMW",
            "part_number": "BM-BT-5512",
            "origin_country": "Germany",
            "price": "4200.00",
        }
        response = self.client.post(reverse("add_product"), payload, follow=True)
        self.assertRedirects(response, reverse("products_list"))
        self.assertEqual(Product.objects.count(), 2)
        self.assertTrue(Product.objects.filter(part_number="BM-BT-5512").exists())

        # Check flash messages
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn("успішно додано", messages_list[0].message)

    def test_add_product_post_invalid(self):
        payload = {
            "name": "",
            "vehicle_brand": "BMW",
            "part_number": "BM-BT-5512",
            "origin_country": "Germany",
            "price": "invalid",
        }
        response = self.client.post(reverse("add_product"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any("заповніть" in m.message for m in messages_list))

    def test_replenish_view(self):
        response = self.client.get(reverse("replenish", kwargs={"count": 3}), follow=True)
        self.assertRedirects(response, reverse("products_list"))
        self.assertEqual(Product.objects.count(), 4)
