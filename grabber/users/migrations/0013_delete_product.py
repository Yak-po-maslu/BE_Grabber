# Generated by Django 5.2 on 2025-07-16 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_cartitem_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
