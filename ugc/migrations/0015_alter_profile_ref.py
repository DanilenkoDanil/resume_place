# Generated by Django 3.2.4 on 2021-09-12 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0014_auto_20210823_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ref',
            field=models.TextField(default='https://t.me/SimpleSMMBot?start=6a7f02c4c8a1cb', verbose_name='Реферальная ссылка'),
        ),
    ]
