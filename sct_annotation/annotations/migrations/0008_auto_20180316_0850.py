# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-16 13:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0007_auto_20180316_0846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='contrast_category',
            new_name='contrast',
        ),
    ]
