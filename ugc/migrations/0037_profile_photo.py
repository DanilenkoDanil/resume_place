# Generated by Django 3.2 on 2022-09-08 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0036_auto_20220907_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
