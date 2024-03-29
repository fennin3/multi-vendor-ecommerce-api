# Generated by Django 3.2.4 on 2022-10-30 23:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UsedCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupons_used', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('code', models.CharField(blank=True, max_length=6, null=True)),
                ('condition', models.CharField(choices=[('newbies', 'newbies'), ('orders', 'orders'), ('amount', 'amount'), ('category', 'category')], max_length=20)),
                ('discount_type', models.CharField(choices=[('PCT', 'PCT'), ('AMT', 'AMT')], default='PCT', max_length=3)),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('min_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('min_orders', models.IntegerField(default=0)),
                ('total_coupons', models.IntegerField()),
                ('available_coupons', models.IntegerField(default=-1)),
                ('no_times', models.IntegerField()),
                ('start_at', models.DateTimeField(blank=True, null=True)),
                ('expire_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.subcategory')),
            ],
        ),
    ]
