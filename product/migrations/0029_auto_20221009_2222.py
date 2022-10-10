# Generated by Django 3.2.4 on 2022-10-09 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_alter_product_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/Category-Avatar/'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/SubCategory-Avatar/'),
        ),
    ]
