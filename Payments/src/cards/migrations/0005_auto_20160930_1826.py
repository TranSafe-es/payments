# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-30 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_card_card_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_id',
            field=models.CharField(max_length=128),
        ),
    ]
