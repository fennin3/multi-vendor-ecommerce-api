# Generated by Django 3.2.4 on 2022-10-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_product_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
