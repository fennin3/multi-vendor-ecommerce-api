# Generated by Django 3.2.4 on 2022-10-20 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0037_flashsalerequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='additional_info',
        ),
    ]
