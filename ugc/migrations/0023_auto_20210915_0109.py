# Generated by Django 3.2.4 on 2021-09-14 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0022_alter_profile_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ref',
            field=models.TextField(default='https://t.me/SimpleSMMBot?start=ed3edd021be52c', verbose_name='Реферальная ссылка'),
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.TextField(verbose_name='Платформа')),
                ('type', models.TextField(verbose_name='Тип заказа')),
                ('count', models.PositiveIntegerField(verbose_name='Количество')),
                ('status', models.TextField(verbose_name='Статус')),
                ('service', models.TextField(verbose_name='Сервис')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ugc.profile', verbose_name='Заказчик')),
            ],
        ),
    ]
