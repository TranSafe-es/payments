# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_id', models.CharField(default=uuid.uuid4, unique=True, max_length=128)),
                ('transaction_id', models.CharField(max_length=128)),
                ('buyer_id', models.CharField(max_length=128)),
                ('seller_id', models.CharField(max_length=128)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('state', models.CharField(default=b'Pending', max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
