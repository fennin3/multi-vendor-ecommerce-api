# Generated by Django 3.2.4 on 2022-10-01 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('order', '0002_alter_order_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
        ),
    ]
