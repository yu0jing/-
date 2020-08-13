# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='menber',
            fields=[
                ('name', models.CharField(max_length=10)),
                ('sex', models.CharField(max_length=5)),
                ('birthday', models.CharField(max_length=10)),
                ('email', models.CharField(primary_key=True, max_length=100, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('doublecheck', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'menber',
            },
        ),
    ]
