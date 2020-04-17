# Generated by Django 3.0.4 on 2020-04-16 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('blog', '0008_remove_articleblogpage_intro_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleblogpage',
            name='intro_image',
            field=models.ForeignKey(blank=True, help_text='Best size for this image will be 1400x400', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image'),
        ),
    ]