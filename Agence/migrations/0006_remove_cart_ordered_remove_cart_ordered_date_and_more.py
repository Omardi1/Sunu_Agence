# Generated by Django 4.1.5 on 2023-01-11 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agence', '0005_rename_order_cart_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='ordered',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='ordered_date',
        ),
        migrations.AddField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
