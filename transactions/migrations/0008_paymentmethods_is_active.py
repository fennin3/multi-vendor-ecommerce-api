# Generated by Django 3.2.4 on 2022-10-05 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_auto_20221005_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethods',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
