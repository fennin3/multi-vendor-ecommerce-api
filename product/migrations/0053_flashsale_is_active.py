# Generated by Django 3.2.4 on 2022-10-25 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0052_flashsalerequest_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashsale',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
