# Generated by Django 4.1.5 on 2023-01-11 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Agence', '0004_remove_order_room_delete_room'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='order',
            new_name='orders',
        ),
    ]
