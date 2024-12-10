# Generated by Django 5.1.3 on 2024-12-10 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="inquiry",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("accepted", "Accepted"),
                    ("rejected", "Rejected"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="listing",
            name="status",
            field=models.CharField(
                choices=[("available", "Available"), ("bought", "Bought")],
                default="available",
                max_length=10,
            ),
        ),
    ]