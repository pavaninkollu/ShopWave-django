# Generated by Django 5.1.2 on 2024-11-08 05:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0006_alter_product_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="specifications",
        ),
    ]
