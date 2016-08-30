# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Op',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('script', models.TextField()),
                ('callback_url', models.CharField(default=b'', max_length=2048, blank=True)),
                ('status', models.CharField(default=b'PENDING', max_length=512, blank=True)),
                ('info', models.TextField(default=b'', blank=True)),
                ('user', models.ForeignKey(related_name='ops', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
