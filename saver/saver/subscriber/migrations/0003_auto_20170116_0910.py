# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 09:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriber', '0002_auto_20170115_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='command',
            name='client',
        ),
        migrations.AddField(
            model_name='command',
            name='connection',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to='subscriber.Connection'),
            preserve_default=False,
        ),
    ]
