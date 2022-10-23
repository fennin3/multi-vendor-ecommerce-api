# Generated by Django 3.2.4 on 2022-10-23 00:21

from django.db import migrations, models
import product.utils


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0047_alter_flashsale_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(default=product.utils.generate_sku, max_length=10),
        ),
    ]