# Generated by Django 3.2.4 on 2022-10-20 11:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0035_flashsale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flashsale',
            name='id',
        ),
        migrations.AddField(
            model_name='flashsale',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
