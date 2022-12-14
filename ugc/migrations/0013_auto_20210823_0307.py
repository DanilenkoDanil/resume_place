# Generated by Django 3.2.4 on 2021-08-23 00:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0012_auto_20210823_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ref',
            field=models.TextField(default='https://t.me/SimpleSMMBot?start=c3db88a363548d', verbose_name='Реферальная ссылка'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='referral',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ugc.profile', verbose_name='Реферал'),
        ),
    ]
