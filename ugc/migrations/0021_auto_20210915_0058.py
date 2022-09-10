# Generated by Django 3.2.4 on 2021-09-14 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0020_auto_20210915_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ref',
            field=models.TextField(default='https://t.me/SimpleSMMBot?start=b0d8f06a78e1e7', verbose_name='Реферальная ссылка'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='referral',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='ugc.profile', verbose_name='Реферал'),
        ),
    ]
