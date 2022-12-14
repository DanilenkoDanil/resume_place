# Generated by Django 3.2.4 on 2021-08-23 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0009_auto_20210823_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='referral',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='ugc.profile', verbose_name='Реферал'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='ref',
            field=models.TextField(default='https://t.me/SimpleSMMBot?start=edbbd01a5d4e9c', verbose_name='Реферальная ссылка'),
        ),
    ]
