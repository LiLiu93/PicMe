# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-15 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('private_chat', '0002_message_visualized'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='visualized',
            field=models.BooleanField(),
        ),
    ]
