# Generated by Django 3.2.4 on 2022-11-02 04:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0005_siteconfiguration_site_percentage'),
        ('transactions', '0002_paymentmethods_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleIncome',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('income_for', models.CharField(choices=[('admin', 'admin'), ('vendor', 'vendor')], max_length=8)),
                ('user', models.UUIDField(blank=True, null=True)),
                ('transaction_ref', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('paid', 'paid')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='administrator.country')),
            ],
        ),
    ]
