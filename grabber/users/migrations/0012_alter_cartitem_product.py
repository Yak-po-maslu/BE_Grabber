# Generated by Django 5.2 on 2025-07-16 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0012_favoritead'),
        ('users', '0011_product_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.ad'),
        ),
    ]
