# Generated by Django 3.2.4 on 2021-07-31 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0003_usersmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotButton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.TextField(verbose_name='Номер кнопки')),
                ('text', models.TextField(verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Кнопка',
                'verbose_name_plural': 'Кнопки',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='ref',
            field=models.TextField(default=0, verbose_name='Реферал'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.BooleanField(default=1, verbose_name='Статус аккаунта'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='BotMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('button', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ugc.botbutton', verbose_name='Кнопка')),
            ],
            options={
                'verbose_name': 'Сообщение Бота',
                'verbose_name_plural': 'Сообщения Бота',
            },
        ),
    ]
