# Generated by Django 3.2.4 on 2022-10-26 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0055_alter_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
