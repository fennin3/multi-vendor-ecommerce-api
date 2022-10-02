# Generated by Django 3.2 on 2022-09-30 15:43

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_vendor_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='shop_name'),
        ),
    ]
