# Generated by Django 2.0.13 on 2019-08-21 11:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20190821_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='description',
        ),
        migrations.AlterField(
            model_name='intern',
            name='app_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 21, 11, 14, 39, 790632), verbose_name='date applied'),
        ),
    ]
