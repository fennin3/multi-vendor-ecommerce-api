# Generated by Django 3.2.4 on 2022-10-05 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20221005_0424'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethods',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentmethods',
            name='uid',
            field=models.CharField(editable=False, max_length=255),
        ),
    ]