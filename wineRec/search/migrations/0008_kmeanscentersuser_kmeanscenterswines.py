# Generated by Django 2.0 on 2019-05-20 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0007_recommend'),
    ]

    operations = [
        migrations.CreateModel(
            name='KmeansCentersUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centers_user', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='KmeansCentersWines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centers_wines', models.TextField()),
            ],
        ),
    ]