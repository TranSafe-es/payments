# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-10 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20160929_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='buyer_card',
            new_name='card_1',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='seller_card',
            new_name='card_2',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='buyer_id',
            new_name='user_id1',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='seller_id',
            new_name='user_id2',
        ),
        migrations.AddField(
            model_name='payment',
            name='description',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
