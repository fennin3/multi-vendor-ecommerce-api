# Generated by Django 3.2.4 on 2022-10-23 18:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_contactmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='id',
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]