# Generated by Django 3.2.4 on 2022-10-09 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_auto_20221009_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
