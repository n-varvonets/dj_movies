# Generated by Django 3.2.6 on 2021-09-06 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20210903_0831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actorordirector',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='actorordirector',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='country_fr',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='tagline_fr',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='title_fr',
        ),
        migrations.RemoveField(
            model_name='movieshots',
            name='description_fr',
        ),
        migrations.RemoveField(
            model_name='movieshots',
            name='title_fr',
        ),
    ]
