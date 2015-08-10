# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URLExp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shorturl', models.URLField(null=True, blank=True)),
                ('httpstat', models.PositiveIntegerField(null=True, blank=True)),
                ('finaldestination', models.URLField(null=True, blank=True)),
                ('pagetitle', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
