# Generated by Django 3.2.4 on 2022-10-25 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0021_auto_20221025_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmedia',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]