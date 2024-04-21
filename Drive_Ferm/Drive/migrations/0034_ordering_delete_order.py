# Generated by Django 4.1 on 2024-04-12 02:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Drive", "0033_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ordering",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                (
                    "price_at_purchase",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("session_id", models.CharField(max_length=100)),
                ("payment_intent", models.CharField(max_length=100)),
                ("payment_status", models.CharField(default="Pending", max_length=50)),
                ("currency", models.CharField(max_length=10)),
                ("email", models.EmailField(max_length=255)),
                ("fullname", models.CharField(max_length=255)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                ("order_date", models.DateTimeField(auto_now_add=True)),
                ("order_status", models.CharField(default="Pending", max_length=50)),
                (
                    "business",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="business_orders",
                        to="Drive.business",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customer_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_orders",
                        to="Drive.product",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Order",
        ),
    ]
