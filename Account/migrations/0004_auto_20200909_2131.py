# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-09 21:31
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_auto_20200909_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=60, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: 917657468565', regex='^(91)\\d{10}$')]),
        ),
    ]