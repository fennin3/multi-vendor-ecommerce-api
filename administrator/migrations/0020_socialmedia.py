# Generated by Django 3.2.4 on 2022-10-25 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0019_auto_20221023_1845'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=1000)),
                ('link', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
