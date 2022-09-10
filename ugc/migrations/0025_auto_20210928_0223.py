# Generated by Django 3.2.4 on 2021-09-27 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0024_auto_20210915_0109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.TextField(verbose_name='Платформа')),
                ('type', models.TextField(verbose_name='Тип заказа')),
                ('product_id', models.TextField(verbose_name='ID услуги')),
                ('service', models.TextField(verbose_name='Сервес')),
                ('price', models.FloatField(verbose_name='Цена за еденицу')),
            ],
            options={
                'verbose_name': 'Сервес',
                'verbose_name_plural': 'Сервесы',
            },
        ),
        migrations.AlterField(
            model_name='profile',
            name='ref',
            field=models.TextField(default='https://t.me/SimpleSMMBot?start=a5c36cc01c48c2', verbose_name='Реферальная ссылка'),
        ),
    ]
