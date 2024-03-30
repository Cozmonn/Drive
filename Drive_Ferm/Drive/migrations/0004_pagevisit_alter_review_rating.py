# Generated by Django 4.1 on 2024-03-29 14:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Drive", "0003_remove_orderitem_order_remove_orderitem_product_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PageVisit",
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
                ("path", models.CharField(max_length=200)),
                ("visit_count", models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.PositiveIntegerField(
                default=0,
                validators=[
                    django.core.validators.MaxValueValidator(5),
                    django.core.validators.MinValueValidator(0),
                ],
            ),
        ),
    ]