# Generated by Django 3.2.4 on 2022-11-02 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0004_auto_20221028_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='site_percentage',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=9),
        ),
    ]
