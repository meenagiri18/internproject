# Generated by Django 5.0.7 on 2025-04-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_payment_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='purchase_order_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
