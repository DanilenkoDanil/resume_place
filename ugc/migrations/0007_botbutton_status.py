# Generated by Django 3.2.4 on 2021-08-02 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0006_auto_20210731_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='botbutton',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Статус'),
            preserve_default=False,
        ),
    ]
