# Generated by Django 3.2.4 on 2022-10-04 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_dealoftheday_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dealoftheday',
            options={'verbose_name': 'Deal the day', 'verbose_name_plural': 'Deal of the day'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='categories',
            new_name='sub_categories',
        ),
    ]
