# Generated by Django 3.2.4 on 2021-09-14 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0021_auto_20210915_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ref',
            field=models.TextField(default='https://t.me/SimpleSMMBot?start=4db6ba63c72c62', verbose_name='Реферальная ссылка'),
        ),
    ]
