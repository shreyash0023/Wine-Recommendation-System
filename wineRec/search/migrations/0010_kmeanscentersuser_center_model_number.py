# Generated by Django 2.0 on 2019-05-20 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0009_auto_20190520_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='kmeanscentersuser',
            name='center_model_number',
            field=models.IntegerField(default=0),
        ),
    ]
