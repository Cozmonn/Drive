# Generated by Django 4.1 on 2024-03-31 10:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Drive", "0013_webcontent_event_created_at_event_activity_icon"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="gallery",
            field=models.ImageField(blank=True, null=True, upload_to="profile_images/"),
        ),
    ]
