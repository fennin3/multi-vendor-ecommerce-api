# Generated by Django 3.2.4 on 2022-10-09 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_auto_20221009_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='avatar',
            field=models.ImageField(upload_to='media/Category-Avatar/'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='avatar',
            field=models.ImageField(upload_to='media/SubCategory-Avatar/'),
        ),
    ]
