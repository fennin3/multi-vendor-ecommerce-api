# Generated by Django 3.2.4 on 2022-10-26 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0023_siteconfiguration_working_hours'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=255)),
                ('visited_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]