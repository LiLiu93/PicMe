# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-15 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('private_chat', '0005_remove_message_visualized'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='visualized',
            field=models.BooleanField(default=False),
        ),
    ]
