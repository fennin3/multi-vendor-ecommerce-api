# Generated by Django 3.2.4 on 2022-10-07 09:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0012_remove_country_states'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='state',
            name='id',
        ),
        migrations.AddField(
            model_name='state',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]