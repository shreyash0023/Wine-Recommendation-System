# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-05 07:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_clusters'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rec_wine_nums', models.IntegerField(max_length=10)),
            ],
        ),
    ]