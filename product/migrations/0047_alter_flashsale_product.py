# Generated by Django 3.2.4 on 2022-10-21 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0046_flashsale_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashsale',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
    ]