# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-30 16:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20160930_1547'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='card',
            unique_together=set([]),
        ),
    ]
