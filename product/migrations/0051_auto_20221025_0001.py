# Generated by Django 3.2.4 on 2022-10-25 00:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0050_flashsale_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flashsalerequest',
            name='days',
        ),
        migrations.AddField(
            model_name='flashsalerequest',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flashsalerequest',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
