# Generated by Django 3.2.4 on 2022-10-03 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_auto_20221003_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
