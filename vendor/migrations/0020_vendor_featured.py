# Generated by Django 3.2.4 on 2022-10-20 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0019_dealofthedayrequest_deal_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]