# Generated by Django 4.0.1 on 2022-01-15 08:19

import api.constants
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_roster'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='first_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='player',
            name='height_feet',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='height_inches',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='hometown',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='last_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='player',
            name='major',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='player_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='weight_pounds',
            field=models.IntegerField(null=True),
        ),
    ]
