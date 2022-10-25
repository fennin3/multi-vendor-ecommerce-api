# Generated by Django 3.2.4 on 2022-10-25 09:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0020_socialmedia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialmedia',
            name='id',
        ),
        migrations.AddField(
            model_name='socialmedia',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]