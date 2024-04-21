# Generated by Django 4.1 on 2024-04-12 00:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Drive", "0031_alter_farm_founded_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="farm",
            name="number_of_employees",
            field=models.IntegerField(
                blank=True,
                help_text="How many people work at the farm",
                null=True,
                verbose_name="Number of Employees",
            ),
        ),
    ]
