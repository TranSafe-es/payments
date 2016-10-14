# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-10 08:53
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_card_defined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_id',
            field=models.CharField(default=uuid.uuid4, max_length=128, unique=True),
        ),
    ]