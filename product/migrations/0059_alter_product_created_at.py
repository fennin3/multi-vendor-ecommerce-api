# Generated by Django 3.2.4 on 2022-10-26 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0058_alter_product_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
