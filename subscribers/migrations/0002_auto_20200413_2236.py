# Generated by Django 3.0.4 on 2020-04-13 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscribers',
            new_name='Subscriber',
        ),
    ]