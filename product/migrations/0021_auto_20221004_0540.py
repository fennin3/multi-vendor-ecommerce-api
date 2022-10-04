# Generated by Django 3.2.4 on 2022-10-04 05:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_review_is_active'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='SubCategory',
        ),
        migrations.CreateModel(
            name='DealOfTheDay',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
