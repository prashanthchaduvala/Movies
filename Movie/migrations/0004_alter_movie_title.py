# Generated by Django 4.0.6 on 2022-11-16 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movie', '0003_cast_movie_userprofile_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='title'),
        ),
    ]
