# Generated by Django 3.2.4 on 2022-10-28 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='blog.category'),
        ),
    ]