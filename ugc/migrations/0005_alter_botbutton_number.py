# Generated by Django 3.2.4 on 2021-07-31 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0004_auto_20210731_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botbutton',
            name='number',
            field=models.PositiveIntegerField(verbose_name='Номер кнопки'),
        ),
    ]
