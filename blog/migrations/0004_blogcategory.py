# Generated by Django 3.0.4 on 2020-04-15 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogauthorsorderable'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(help_text='Slug to identify posts by category', max_length=255, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Blog category',
                'verbose_name_plural': 'Blog categories',
                'ordering': ['name'],
            },
        ),
    ]