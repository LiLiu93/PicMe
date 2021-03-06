# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 05:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('post_title', models.CharField(max_length=200)),
                ('post_description', models.TextField(max_length=160)),
                ('post_picture', models.ImageField(upload_to=posts.models.post_directory_path)),
                ('show', models.BooleanField(default=True)),
                ('likes', models.ManyToManyField(related_name='likes_posts', to=settings.AUTH_USER_MODEL)),
                ('post_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city', to='address.City')),
                ('post_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='address.State')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
