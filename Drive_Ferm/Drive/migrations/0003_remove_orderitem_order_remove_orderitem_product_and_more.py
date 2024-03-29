# Generated by Django 4.1 on 2024-03-27 22:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Drive", "0002_alter_business_options_alter_customer_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="order",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="product",
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="product_images/"),
        ),
        migrations.DeleteModel(
            name="Order",
        ),
        migrations.DeleteModel(
            name="OrderItem",
        ),
    ]
