# Generated by Django 3.0.4 on 2020-04-16 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_articleblogpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleblogpage',
            name='intro_image',
        ),
    ]