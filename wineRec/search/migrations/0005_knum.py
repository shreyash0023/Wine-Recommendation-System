# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-04 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_classify'),
    ]

    operations = [
        migrations.CreateModel(
            name='knum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(max_length=10)),
            ],
        ),
    ]