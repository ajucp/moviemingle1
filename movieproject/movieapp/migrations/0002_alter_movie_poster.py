# Generated by Django 4.2.8 on 2024-03-03 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='posters/'),
        ),
    ]
