# Generated by Django 2.0 on 2019-05-21 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0010_kmeanscentersuser_center_model_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistanceMetric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance_metric', models.IntegerField(default=0)),
            ],
        ),
    ]