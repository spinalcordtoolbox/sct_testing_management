# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-24 03:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='filename',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='labeledimage',
            name='filename',
            field=models.CharField(max_length=512),
        ),
    ]
